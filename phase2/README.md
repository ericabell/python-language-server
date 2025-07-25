# Phase 2: Core Language Features

## Learning Goals
- Document synchronization and text management
- Workspace and document URI handling
- Basic language analysis concepts
- Python syntax error detection using AST
- Hover information implementation

## Mini-Projects
1. **URI Handler**: Build a utility that can convert between file paths and LSP URIs
2. **Text Buffer Manager**: Create a class that tracks document content and changes
3. **Python Syntax Checker**: Use Python's AST module to detect syntax errors
4. **Simple Hover Provider**: Return basic information for Python keywords and built-ins

## Implementation Goals
1. **Document Sync**: Track open documents and their changes using textDocument/didOpen, didChange, didClose
2. **Diagnostics**: Implement basic Python syntax error detection with publishDiagnostics
3. **Hover Information**: Provide simple hover tooltips for Python keywords and built-ins
4. **Error Reporting**: Build a robust error handling and reporting system

## Progress Tracking
- [ ] Completed pre-reading materials
- [ ] Built URI Handler
- [ ] Built Text Buffer Manager
- [ ] Built Python Syntax Checker
- [ ] Built Simple Hover Provider
- [ ] Implemented document synchronization
- [ ] Implemented diagnostics
- [ ] Implemented hover information
- [ ] Implemented error reporting
- [ ] Passed all knowledge checks

## Knowledge Checks
- [ ] How does the server stay synchronized with document changes?
- [ ] What's the difference between push and pull diagnostic models?
- [ ] Implement incremental vs full document synchronization
- [ ] Create a test suite for your document synchronization

## Notes
(Add your learning notes and insights here as you progress)