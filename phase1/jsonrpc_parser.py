"""
JSON-RPC 2.0 Message Parser

This module provides functionality to parse and validate JSON-RPC 2.0 messages.
"""

import json
from typing import Dict, Any, Union, Optional
from enum import Enum

class JSONRPCErrorCodes(Enum):
    """Enumeration of JSON-RPC error codes"""
    PARSE_ERROR = -32700
    INVALID_REQUEST = -32600
    METHOD_NOT_FOUND = -32601
    INVALID_PARAMS = -32602
    INTERNAL_ERROR = -32603


class MessageType(Enum):
    """Enumeration of JSON-RPC message types"""
    REQUEST = "request"
    RESPONSE = "response" 
    NOTIFICATION = "notification"
    PARSE_ERROR = "parse_error"
    INVALID_REQUEST = "invalid_request"


class ParseResult:
    """Result of parsing a JSON-RPC message"""
    def __init__(self, message_type: MessageType, data: Optional[Dict[str, Any]] = None, 
                 error_code: Optional[int] = None, error_message: Optional[str] = None):
        self.message_type = message_type
        self.data = data
        self.error_code = error_code
        self.error_message = error_message
    
    def is_valid(self) -> bool:
        """Returns True if the message was parsed successfully"""
        return self.message_type in [MessageType.REQUEST, MessageType.RESPONSE, MessageType.NOTIFICATION]
    
    def __repr__(self):
        if self.is_valid():
            return f"ParseResult(type={self.message_type.value}, data={self.data})"
        else:
            return f"ParseResult(type={self.message_type.value}, error={self.error_code}: {self.error_message})"


def parse_jsonrpc_message(json_string: str) -> ParseResult:
    """
    Parse a JSON string and determine if it's a valid JSON-RPC 2.0 message.
    
    Args:
        json_string: The JSON string to parse
        
    Returns:
        ParseResult object containing the message type, data, and any errors
    """
    # Step 1: Try to parse JSON
    try:
        data = json.loads(json_string)
    except json.JSONDecodeError as e:
        return ParseResult(
            MessageType.PARSE_ERROR,
            error_code=JSONRPCErrorCodes.PARSE_ERROR.value,
            error_message=f"Parse error: {str(e)}"
        )
    
    # Step 2: Check required jsonrpc field
    if not isinstance(data, dict):
        return ParseResult(
            MessageType.INVALID_REQUEST,
            error_code=JSONRPCErrorCodes.INVALID_REQUEST.value,
            error_message="Invalid Request: message must be a JSON object"
        )

    if data.get("jsonrpc") != "2.0":
        return ParseResult(
            MessageType.INVALID_REQUEST,
            error_code=JSONRPCErrorCodes.INVALID_REQUEST.value,
            error_message="Invalid Request: jsonrpc field must be '2.0'"
        )
    
    # Step 3: Determine message type
    def _is_request(data: dict) -> bool:
        """Request: has method, id, optionally params. No result/error."""
        required = {"method", "id"}
        forbidden = {"result", "error"}
        return (required.issubset(data.keys()) and 
                forbidden.isdisjoint(data.keys()))

    def _is_notification(data: dict) -> bool:
        """Notification: has method, optionally params. No id, result, or error."""
        required = {"method"}
        forbidden = {"id", "result", "error"}
        return (required.issubset(data.keys()) and 
                forbidden.isdisjoint(data.keys()))

    def _is_response(data: dict) -> bool:
        """Response: has id and exactly one of result/error. No method."""
        has_id = "id" in data
        has_method = "method" in data
        has_result = "result" in data
        has_error = "error" in data
        
        return (has_id and not has_method and 
                (has_result ^ has_error))  # XOR: exactly one of result/error

    # Determine message type
    if _is_request(data):
        message_type = MessageType.REQUEST
    elif _is_notification(data):
        message_type = MessageType.NOTIFICATION
    elif _is_response(data):
        message_type = MessageType.RESPONSE
    else:
        return ParseResult(
            MessageType.INVALID_REQUEST,
            error_code=JSONRPCErrorCodes.INVALID_REQUEST.value,
            error_message="Invalid Request: message structure doesn't match any valid JSON-RPC 2.0 type"
        )
    
    # Step 4: Validate required fields
    if message_type in [MessageType.REQUEST, MessageType.NOTIFICATION]:
        # Validate method field
        if not isinstance(data.get("method"), str):
            return ParseResult(
                MessageType.INVALID_REQUEST,
                error_code=JSONRPCErrorCodes.INVALID_REQUEST.value,
                error_message="Invalid Request: method must be a string"
            )

    if message_type in [MessageType.REQUEST, MessageType.RESPONSE]:
        # Validate id field  
        id_value = data.get("id")
        if not isinstance(id_value, (str, int, float, type(None))):
            return ParseResult(
                MessageType.INVALID_REQUEST,
                error_code=JSONRPCErrorCodes.INVALID_REQUEST.value,
                error_message="Invalid Request: id must be a string, number, or null"
            )

    # For responses with error, validate error is an object
    if message_type == MessageType.RESPONSE and "error" in data:
        if not isinstance(data.get("error"), dict):
            return ParseResult(
                MessageType.INVALID_REQUEST,
                error_code=JSONRPCErrorCodes.INVALID_REQUEST.value,
                error_message="Invalid Request: error must be an object"
            )
    
    # Step 5: Return success
    return ParseResult(
        message_type=message_type,
        data=data
    )


if __name__ == "__main__":
    # Test cases based on real JSON-RPC examples
    test_cases = [
        # Valid request
        ('{"jsonrpc": "2.0", "method": "initialize", "params": {"rootUri": null}, "id": 1}', "Valid REQUEST"),
        
        # Valid notification  
        ('{"jsonrpc": "2.0", "method": "initialized", "params": {}}', "Valid NOTIFICATION"),
        
        # Valid response with result
        ('{"jsonrpc": "2.0", "result": {"capabilities": {}}, "id": 1}', "Valid RESPONSE (result)"),
        
        # Valid response with error
        ('{"jsonrpc": "2.0", "error": {"code": -32602, "message": "Invalid params"}, "id": 1}', "Valid RESPONSE (error)"),
        
        # Invalid - missing jsonrpc
        ('{"method": "test", "id": 1}', "Missing jsonrpc field"),
        
        # Invalid - wrong jsonrpc version
        ('{"jsonrpc": "1.0", "method": "test", "id": 1}', "Wrong jsonrpc version"),
        
        # Invalid JSON
        ('{"jsonrpc": "2.0", "method": "test", "id": 1', "Malformed JSON"),
        
        # Invalid - both result and error
        ('{"jsonrpc": "2.0", "result": "success", "error": {"code": -1}, "id": 1}', "Response with both result and error"),
    ]
    
    print("Testing JSON-RPC Message Parser")
    print("=" * 50)
    
    for i, (test_case, description) in enumerate(test_cases, 1):
        print(f"\nTest {i}: {description}")
        print(f"Input: {test_case[:60]}{'...' if len(test_case) > 60 else ''}")
        result = parse_jsonrpc_message(test_case)
        print(f"Result: {result}")
        
    print("\n" + "=" * 50)
    print("Testing complete!")