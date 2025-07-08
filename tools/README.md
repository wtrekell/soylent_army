# Central Tools Library

This directory contains the centralized collection of production-ready tools for the Soylent Army CrewAI implementation. These tools have been carefully selected and tested to provide reliable functionality without complex dependencies.

## Available Tools

### Core File Operations
- **FileReadTool** - Read files, CSV data, and text-based content
- **FileWriterTool** - Create and write output files with various formats
- **DirectoryReadTool** - Browse and explore directory structures

### Web Research & Search
- **SerperDevTool** - Real-time internet search capabilities (requires SERPER_API_KEY)

## Tool Integration

Tools are imported from this central location into individual crews to avoid duplication and ensure consistency. Each tool has been verified to work without complex dependency requirements.

### Usage Example

```python
# Import from central tools library
import sys
import os
sys.path.append('/Users/williamtrekell/Documents/git_repos/soylent_army')
from tools.serper_dev_tool.serper_dev_tool import SerperDevTool
from tools.file_read_tool.file_read_tool import FileReadTool
from tools.file_writer_tool.file_writer_tool import FileWriterTool
from tools.directory_read_tool.directory_read_tool import DirectoryReadTool

# Initialize tools in your crew
serper_tool = SerperDevTool()
file_read_tool = FileReadTool()
file_write_tool = FileWriterTool()
directory_tool = DirectoryReadTool()
```

## Tool Selection Criteria

Tools in this library have been selected based on:
1. **Minimal Dependencies** - No complex external requirements
2. **Production Ready** - Tested and verified functionality
3. **CrewAI Compatible** - Proper integration with CrewAI framework
4. **Performance** - Efficient execution without bloat

## Adding New Tools

When adding new tools:
1. Verify minimal dependency requirements
2. Test functionality in isolation
3. Update this README with tool description
4. Add to central `__init__.py` file
5. Document any API keys or configuration requirements

## Notes

- **CSV Processing**: CSV files can be read directly using FileReadTool since they are text-based
- **PDF Processing**: Currently requires embedchain dependency which has installation complexities
- **API Keys**: SerperDevTool requires SERPER_API_KEY in environment variables