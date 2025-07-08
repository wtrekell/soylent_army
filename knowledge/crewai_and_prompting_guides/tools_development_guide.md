# Complete Guide to AI Agent Tools Development

## Table of Contents
1. [Introduction to AI Agent Tools](#introduction)
2. [Core Concepts & Architecture](#core-concepts)
3. [Tool Creation Methods](#creation-methods)
4. [Framework-Specific Implementation](#frameworks)
5. [Advanced Tool Patterns](#advanced-patterns)
6. [Integration Strategies](#integration)
7. [Testing & Optimization](#testing)
8. [Security & Best Practices](#security)
9. [Enterprise Considerations](#enterprise)
10. [Resources & Examples](#resources)

## Introduction to AI Agent Tools {#introduction}

### What Are AI Agent Tools?

AI agent tools are functions or capabilities that agents can utilize to perform various actions beyond their base language model capabilities. They extend agent functionality by enabling interaction with external systems, data sources, APIs, and real-world applications.

### Why Tools Matter

- **Real-World Integration**: Connect AI reasoning to actual data and functions
- **Capability Extension**: Go beyond pre-trained knowledge limitations
- **Dynamic Interaction**: Enable real-time data access and manipulation
- **Specialized Functions**: Perform complex calculations, API calls, and system operations

### Tool Categories

1. **Data Access Tools**: Database queries, file operations, web scraping
2. **Communication Tools**: Email, messaging, notifications
3. **Computation Tools**: Mathematical calculations, data analysis
4. **Integration Tools**: API connections, system integrations
5. **Content Tools**: Document generation, image processing, media manipulation

## Core Concepts & Architecture {#core-concepts}

### Tool Components

Every effective AI agent tool consists of:

1. **Name**: Clear, descriptive identifier
2. **Description**: Natural language explanation for LLM decision-making
3. **Parameters**: Input schema and validation
4. **Function Logic**: Core execution code
5. **Error Handling**: Robust failure management
6. **Documentation**: Usage examples and specifications

### Tool Selection Process

The LLM uses tools through this decision process:
1. **Task Analysis**: Understand the required action
2. **Tool Identification**: Match task to available tools
3. **Parameter Extraction**: Determine required inputs
4. **Execution**: Call the tool with parameters
5. **Result Processing**: Interpret and use tool output

### Architecture Patterns

#### Function-Based Tools
```python
def weather_tool(location: str) -> dict:
    """Get current weather for a location."""
    # Tool implementation
    return weather_data
```

#### Class-Based Tools
```python
class DatabaseTool:
    def __init__(self, connection_string):
        self.db = connect(connection_string)
    
    def query(self, sql: str) -> list:
        """Execute SQL query and return results."""
        return self.db.execute(sql).fetchall()
```

#### Service-Based Tools
```python
class APITool:
    def __init__(self, base_url, api_key):
        self.client = APIClient(base_url, api_key)
    
    def call_endpoint(self, endpoint: str, params: dict) -> dict:
        """Make API call to specified endpoint."""
        return self.client.request(endpoint, params)
```

## Tool Creation Methods {#creation-methods}

### Method 1: Using the @tool Decorator (Recommended)

The simplest and most widely recommended approach across frameworks:

```python
from langchain.tools import tool

@tool
def calculate_area(length: float, width: float) -> float:
    """Calculate the area of a rectangle.
    
    Args:
        length: The length of the rectangle
        width: The width of the rectangle
    
    Returns:
        The area of the rectangle
    """
    return length * width
```

**Advantages:**
- Minimal boilerplate code
- Automatic schema generation
- Type hint integration
- Easy to understand and maintain

### Method 2: Subclassing BaseTool

For maximum control and custom behavior:

```python
from langchain.tools import BaseTool
from pydantic import BaseModel, Field

class CalculatorInput(BaseModel):
    operation: str = Field(description="The mathematical operation to perform")
    operands: list[float] = Field(description="The numbers to operate on")

class CalculatorTool(BaseTool):
    name = "calculator"
    description = "Performs mathematical calculations"
    args_schema: Type[BaseModel] = CalculatorInput
    
    def _run(self, operation: str, operands: list[float]) -> str:
        """Execute the calculation."""
        if operation == "add":
            return str(sum(operands))
        elif operation == "multiply":
            return str(math.prod(operands))
        # Add more operations
        else:
            return "Unsupported operation"
    
    async def _arun(self, operation: str, operands: list[float]) -> str:
        """Async version of the tool."""
        return self._run(operation, operands)
```

**Advantages:**
- Full control over tool behavior
- Custom validation logic
- Advanced error handling
- Async support

### Method 3: Using StructuredTool

For tools requiring both sync and async implementations:

```python
from langchain.tools import StructuredTool

def sync_web_search(query: str) -> str:
    """Synchronous web search."""
    # Implementation
    return search_results

async def async_web_search(query: str) -> str:
    """Asynchronous web search."""
    # Async implementation
    return search_results

web_search_tool = StructuredTool.from_function(
    func=sync_web_search,
    coroutine=async_web_search,
    name="web_search",
    description="Search the web for information"
)
```

## Framework-Specific Implementation {#frameworks}

### LangChain Tools

#### Basic Tool Creation
```python
from langchain.tools import Tool

def get_stock_price(symbol: str) -> str:
    """Get current stock price for a symbol."""
    # API call to stock service
    return f"${price}"

stock_tool = Tool(
    name="Stock Price",
    func=get_stock_price,
    description="Get current stock price for a given symbol"
)
```

#### Tool with Validation
```python
from langchain.tools import BaseTool
from pydantic import BaseModel, validator

class StockInput(BaseModel):
    symbol: str
    
    @validator('symbol')
    def validate_symbol(cls, v):
        if not v.isalpha() or len(v) > 5:
            raise ValueError('Invalid stock symbol')
        return v.upper()

class StockTool(BaseTool):
    name = "stock_price"
    description = "Get stock price for a symbol"
    args_schema = StockInput
    
    def _run(self, symbol: str) -> str:
        # Implementation with validated input
        return get_stock_data(symbol)
```

### CrewAI Tools

#### Simple Tool Definition
```python
from crewai_tools import tool

@tool
def file_reader(file_path: str) -> str:
    """Read and return the contents of a file.
    
    Args:
        file_path: Path to the file to read
    """
    with open(file_path, 'r') as file:
        return file.read()
```

#### BaseTool Inheritance
```python
from crewai_tools import BaseTool

class DatabaseQueryTool(BaseTool):
    name: str = "Database Query"
    description: str = "Execute SQL queries on the database"
    
    def _run(self, query: str) -> str:
        # Database connection and query execution
        results = self.db.execute(query)
        return self.format_results(results)
```

### Custom Framework Tools

#### Generic Tool Interface
```python
class GenericTool:
    def __init__(self, name: str, description: str, func: callable):
        self.name = name
        self.description = description
        self.func = func
    
    def execute(self, **kwargs):
        try:
            return self.func(**kwargs)
        except Exception as e:
            return f"Error: {str(e)}"
    
    def get_schema(self):
        """Return tool schema for LLM."""
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self._extract_parameters()
        }
```

## Advanced Tool Patterns {#advanced-patterns}

### Stateful Tools

Tools that maintain state across calls:

```python
class SessionTool(BaseTool):
    def __init__(self):
        self.session_data = {}
    
    name = "session_manager"
    description = "Manage session state across interactions"
    
    def _run(self, action: str, key: str = None, value: str = None) -> str:
        if action == "set" and key and value:
            self.session_data[key] = value
            return f"Set {key} = {value}"
        elif action == "get" and key:
            return self.session_data.get(key, "Key not found")
        elif action == "list":
            return str(list(self.session_data.keys()))
        return "Invalid action"
```

### Composite Tools

Tools that combine multiple operations:

```python
class DataAnalysisTool(BaseTool):
    name = "data_analysis"
    description = "Perform comprehensive data analysis"
    
    def _run(self, data_source: str, analysis_type: str) -> str:
        # Load data
        data = self.load_data(data_source)
        
        # Perform analysis based on type
        if analysis_type == "summary":
            return self.generate_summary(data)
        elif analysis_type == "trends":
            return self.identify_trends(data)
        elif analysis_type == "anomalies":
            return self.detect_anomalies(data)
        
    def load_data(self, source: str):
        # Data loading logic
        pass
    
    def generate_summary(self, data):
        # Summary generation logic
        pass
```

### Async Tools

For non-blocking operations:

```python
import asyncio
from langchain.tools import BaseTool

class AsyncWebTool(BaseTool):
    name = "async_web_fetch"
    description = "Asynchronously fetch web content"
    
    def _run(self, url: str) -> str:
        # Synchronous wrapper for async operation
        return asyncio.run(self._arun(url))
    
    async def _arun(self, url: str) -> str:
        """Async implementation."""
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return await response.text()
```

### Conditional Tools

Tools that adapt behavior based on context:

```python
class AdaptiveTool(BaseTool):
    name = "adaptive_processor"
    description = "Process data with adaptive algorithms"
    
    def _run(self, data: str, context: str = None) -> str:
        # Choose processing method based on context
        if context == "production":
            return self.production_process(data)
        elif context == "development":
            return self.development_process(data)
        else:
            return self.default_process(data)
```

## Integration Strategies {#integration}

### API Integration Patterns

#### REST API Tool
```python
import requests
from langchain.tools import tool

@tool
def rest_api_call(endpoint: str, method: str = "GET", data: dict = None) -> str:
    """Make REST API calls to external services.
    
    Args:
        endpoint: The API endpoint URL
        method: HTTP method (GET, POST, PUT, DELETE)
        data: Request payload for POST/PUT requests
    """
    try:
        response = requests.request(method, endpoint, json=data)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return f"API call failed: {str(e)}"
```

#### GraphQL Integration
```python
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

@tool
def graphql_query(query: str, variables: dict = None) -> str:
    """Execute GraphQL queries.
    
    Args:
        query: GraphQL query string
        variables: Query variables
    """
    transport = RequestsHTTPTransport(url="https://api.example.com/graphql")
    client = Client(transport=transport)
    
    try:
        result = client.execute(gql(query), variable_values=variables)
        return str(result)
    except Exception as e:
        return f"GraphQL query failed: {str(e)}"
```

### Database Integration

#### SQL Database Tool
```python
import sqlite3
from langchain.tools import tool

@tool
def sql_query(query: str, database_path: str = "default.db") -> str:
    """Execute SQL queries on the database.
    
    Args:
        query: SQL query to execute
        database_path: Path to the database file
    """
    try:
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()
        cursor.execute(query)
        
        if query.strip().upper().startswith('SELECT'):
            results = cursor.fetchall()
            return str(results)
        else:
            conn.commit()
            return f"Query executed successfully. Rows affected: {cursor.rowcount}"
    except sqlite3.Error as e:
        return f"Database error: {str(e)}"
    finally:
        conn.close()
```

#### NoSQL Database Tool
```python
from pymongo import MongoClient
from langchain.tools import tool

@tool
def mongodb_query(collection: str, filter_dict: dict, operation: str = "find") -> str:
    """Query MongoDB collections.
    
    Args:
        collection: Collection name
        filter_dict: Query filter
        operation: Operation type (find, insert, update, delete)
    """
    client = MongoClient('mongodb://localhost:27017/')
    db = client['myapp']
    coll = db[collection]
    
    try:
        if operation == "find":
            results = list(coll.find(filter_dict))
            return str(results)
        elif operation == "insert":
            result = coll.insert_one(filter_dict)
            return f"Inserted document with ID: {result.inserted_id}"
        # Add other operations
    except Exception as e:
        return f"MongoDB error: {str(e)}"
```

### File System Operations

#### File Management Tool
```python
import os
import shutil
from pathlib import Path

@tool
def file_operations(operation: str, path: str, content: str = None, destination: str = None) -> str:
    """Perform file system operations.
    
    Args:
        operation: Operation type (read, write, copy, move, delete, list)
        path: File or directory path
        content: Content for write operations
        destination: Destination path for copy/move operations
    """
    try:
        path_obj = Path(path)
        
        if operation == "read":
            return path_obj.read_text()
        elif operation == "write":
            path_obj.write_text(content)
            return f"Written to {path}"
        elif operation == "copy":
            shutil.copy2(path, destination)
            return f"Copied {path} to {destination}"
        elif operation == "move":
            shutil.move(path, destination)
            return f"Moved {path} to {destination}"
        elif operation == "delete":
            if path_obj.is_file():
                path_obj.unlink()
            else:
                shutil.rmtree(path)
            return f"Deleted {path}"
        elif operation == "list":
            items = [item.name for item in path_obj.iterdir()]
            return str(items)
    except Exception as e:
        return f"File operation error: {str(e)}"
```

## Testing & Optimization {#testing}

### Unit Testing Tools

```python
import unittest
from unittest.mock import patch, MagicMock

class TestWeatherTool(unittest.TestCase):
    def setUp(self):
        self.weather_tool = WeatherTool()
    
    @patch('requests.get')
    def test_weather_api_call(self, mock_get):
        # Mock API response
        mock_response = MagicMock()
        mock_response.json.return_value = {"temperature": 72, "condition": "sunny"}
        mock_get.return_value = mock_response
        
        # Test tool execution
        result = self.weather_tool._run("New York")
        
        # Assertions
        self.assertIn("72", result)
        self.assertIn("sunny", result)
        mock_get.assert_called_once()
    
    def test_invalid_location(self):
        result = self.weather_tool._run("")
        self.assertIn("error", result.lower())
```

### Integration Testing

```python
class TestToolIntegration(unittest.TestCase):
    def test_tool_with_agent(self):
        # Create agent with tools
        agent = create_agent([weather_tool, calculator_tool])
        
        # Test tool selection and execution
        response = agent.run("What's the weather in Seattle and calculate 15 * 20?")
        
        # Verify both tools were used
        self.assertIn("weather", response.lower())
        self.assertIn("300", response)  # 15 * 20 = 300
```

### Performance Testing

```python
import time
import statistics

def benchmark_tool(tool, inputs, iterations=100):
    """Benchmark tool performance."""
    execution_times = []
    
    for _ in range(iterations):
        start_time = time.time()
        tool._run(**inputs)
        execution_time = time.time() - start_time
        execution_times.append(execution_time)
    
    return {
        "mean": statistics.mean(execution_times),
        "median": statistics.median(execution_times),
        "min": min(execution_times),
        "max": max(execution_times)
    }
```

### Error Handling Testing

```python
def test_tool_error_handling():
    """Test tool behavior under error conditions."""
    
    # Test network errors
    with patch('requests.get', side_effect=requests.ConnectionError()):
        result = api_tool._run("test_endpoint")
        assert "error" in result.lower()
    
    # Test invalid inputs
    result = calculator_tool._run("invalid_operation", [])
    assert "error" in result.lower() or "unsupported" in result.lower()
    
    # Test timeout scenarios
    with patch('requests.get', side_effect=requests.Timeout()):
        result = slow_api_tool._run("test_endpoint")
        assert "timeout" in result.lower()
```

## Security & Best Practices {#security}

### Input Validation

```python
from pydantic import BaseModel, validator
import re

class SecureToolInput(BaseModel):
    file_path: str
    content: str = None
    
    @validator('file_path')
    def validate_file_path(cls, v):
        # Prevent path traversal attacks
        if ".." in v or v.startswith("/"):
            raise ValueError("Invalid file path")
        
        # Only allow specific file extensions
        allowed_extensions = ['.txt', '.json', '.csv']
        if not any(v.endswith(ext) for ext in allowed_extensions):
            raise ValueError("File type not allowed")
        
        return v
    
    @validator('content')
    def validate_content(cls, v):
        if v and len(v) > 10000:  # 10KB limit
            raise ValueError("Content too large")
        return v
```

### SQL Injection Prevention

```python
@tool
def secure_sql_query(table: str, conditions: dict) -> str:
    """Execute parameterized SQL queries safely.
    
    Args:
        table: Table name (validated against whitelist)
        conditions: WHERE conditions as key-value pairs
    """
    # Whitelist of allowed tables
    allowed_tables = ['users', 'products', 'orders']
    if table not in allowed_tables:
        return "Error: Table not allowed"
    
    # Build parameterized query
    placeholders = " AND ".join([f"{key} = ?" for key in conditions.keys()])
    query = f"SELECT * FROM {table} WHERE {placeholders}"
    
    try:
        cursor.execute(query, list(conditions.values()))
        return str(cursor.fetchall())
    except Exception as e:
        return f"Query error: {str(e)}"
```

### API Key Management

```python
import os
from functools import wraps

def require_api_key(key_name: str):
    """Decorator to require API key for tool execution."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            api_key = os.getenv(key_name)
            if not api_key:
                return f"Error: {key_name} not configured"
            return func(*args, **kwargs)
        return wrapper
    return decorator

@tool
@require_api_key('WEATHER_API_KEY')
def secure_weather_tool(location: str) -> str:
    """Weather tool with API key validation."""
    api_key = os.getenv('WEATHER_API_KEY')
    # Use API key in request
    return fetch_weather(location, api_key)
```

### Rate Limiting

```python
import time
from functools import wraps

class RateLimiter:
    def __init__(self, max_calls: int, time_window: int):
        self.max_calls = max_calls
        self.time_window = time_window
        self.calls = []
    
    def is_allowed(self):
        now = time.time()
        # Remove old calls outside time window
        self.calls = [call for call in self.calls if now - call < self.time_window]
        
        if len(self.calls) >= self.max_calls:
            return False
        
        self.calls.append(now)
        return True

def rate_limit(max_calls: int, time_window: int):
    """Rate limiting decorator for tools."""
    limiter = RateLimiter(max_calls, time_window)
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not limiter.is_allowed():
                return "Error: Rate limit exceeded"
            return func(*args, **kwargs)
        return wrapper
    return decorator

@tool
@rate_limit(max_calls=10, time_window=60)  # 10 calls per minute
def rate_limited_api_tool(endpoint: str) -> str:
    """API tool with rate limiting."""
    return make_api_call(endpoint)
```

## Enterprise Considerations {#enterprise}

### Logging and Monitoring

```python
import logging
from datetime import datetime

class MonitoredTool(BaseTool):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = logging.getLogger(f"tool.{self.name}")
    
    def _run(self, *args, **kwargs):
        start_time = datetime.now()
        self.logger.info(f"Tool execution started: {self.name}")
        
        try:
            result = self._execute(*args, **kwargs)
            execution_time = (datetime.now() - start_time).total_seconds()
            
            self.logger.info(f"Tool execution completed: {self.name}, "
                           f"execution_time: {execution_time}s")
            return result
            
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            self.logger.error(f"Tool execution failed: {self.name}, "
                            f"error: {str(e)}, execution_time: {execution_time}s")
            raise
    
    def _execute(self, *args, **kwargs):
        # Override in subclasses
        raise NotImplementedError
```

### Configuration Management

```python
from typing import Dict, Any
import json

class ConfigurableTool(BaseTool):
    def __init__(self, config_path: str = None, **kwargs):
        super().__init__(**kwargs)
        self.config = self.load_config(config_path)
    
    def load_config(self, config_path: str) -> Dict[str, Any]:
        """Load tool configuration from file."""
        if config_path and os.path.exists(config_path):
            with open(config_path, 'r') as f:
                return json.load(f)
        return self.default_config()
    
    def default_config(self) -> Dict[str, Any]:
        """Return default configuration."""
        return {
            "timeout": 30,
            "retry_attempts": 3,
            "cache_enabled": True
        }
    
    def update_config(self, **kwargs):
        """Update configuration at runtime."""
        self.config.update(kwargs)
```

### Caching Strategy

```python
import hashlib
import pickle
from functools import wraps

class ToolCache:
    def __init__(self, max_size: int = 1000, ttl: int = 3600):
        self.cache = {}
        self.access_times = {}
        self.max_size = max_size
        self.ttl = ttl
    
    def get_key(self, func_name: str, args: tuple, kwargs: dict) -> str:
        """Generate cache key from function name and arguments."""
        key_data = f"{func_name}:{args}:{sorted(kwargs.items())}"
        return hashlib.md5(key_data.encode()).hexdigest()
    
    def get(self, key: str):
        """Get cached result if valid."""
        if key in self.cache:
            cached_time, result = self.cache[key]
            if time.time() - cached_time < self.ttl:
                self.access_times[key] = time.time()
                return result
            else:
                del self.cache[key]
                del self.access_times[key]
        return None
    
    def set(self, key: str, value):
        """Set cached result with eviction if needed."""
        if len(self.cache) >= self.max_size:
            # Evict least recently used
            oldest_key = min(self.access_times.keys(), 
                           key=lambda k: self.access_times[k])
            del self.cache[oldest_key]
            del self.access_times[oldest_key]
        
        self.cache[key] = (time.time(), value)
        self.access_times[key] = time.time()

# Global cache instance
tool_cache = ToolCache()

def cache_result(func):
    """Decorator to cache tool results."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        cache_key = tool_cache.get_key(func.__name__, args, kwargs)
        cached_result = tool_cache.get(cache_key)
        
        if cached_result is not None:
            return cached_result
        
        result = func(*args, **kwargs)
        tool_cache.set(cache_key, result)
        return result
    
    return wrapper
```

## Resources & Examples {#resources}

### Complete Tool Examples

#### Web Scraping Tool
```python
import requests
from bs4 import BeautifulSoup
from langchain.tools import tool

@tool
def web_scraper(url: str, selector: str = None) -> str:
    """Scrape content from web pages.
    
    Args:
        url: URL to scrape
        selector: CSS selector for specific elements
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        if selector:
            elements = soup.select(selector)
            return '\n'.join([elem.get_text().strip() for elem in elements])
        else:
            return soup.get_text().strip()
            
    except Exception as e:
        return f"Scraping failed: {str(e)}"
```

#### Email Tool
```python
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

@tool
def send_email(to: str, subject: str, body: str, smtp_server: str = "smtp.gmail.com") -> str:
    """Send email via SMTP.
    
    Args:
        to: Recipient email address
        subject: Email subject
        body: Email body
        smtp_server: SMTP server address
    """
    try:
        msg = MIMEMultipart()
        msg['From'] = os.getenv('EMAIL_USER')
        msg['To'] = to
        msg['Subject'] = subject
        
        msg.attach(MIMEText(body, 'plain'))
        
        server = smtplib.SMTP(smtp_server, 587)
        server.starttls()
        server.login(os.getenv('EMAIL_USER'), os.getenv('EMAIL_PASSWORD'))
        server.send_message(msg)
        server.quit()
        
        return f"Email sent successfully to {to}"
        
    except Exception as e:
        return f"Email failed: {str(e)}"
```

#### Data Visualization Tool
```python
import matplotlib.pyplot as plt
import pandas as pd
import base64
from io import BytesIO

@tool
def create_chart(data: str, chart_type: str = "bar", title: str = "Chart") -> str:
    """Create data visualizations.
    
    Args:
        data: JSON string with chart data
        chart_type: Type of chart (bar, line, pie, scatter)
        title: Chart title
    """
    try:
        import json
        chart_data = json.loads(data)
        df = pd.DataFrame(chart_data)
        
        plt.figure(figsize=(10, 6))
        
        if chart_type == "bar":
            plt.bar(df.index, df.iloc[:, 0])
        elif chart_type == "line":
            plt.plot(df.index, df.iloc[:, 0])
        elif chart_type == "pie":
            plt.pie(df.iloc[:, 0], labels=df.index)
        elif chart_type == "scatter":
            plt.scatter(df.iloc[:, 0], df.iloc[:, 1])
        
        plt.title(title)
        
        # Save to base64 string
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()
        
        graphic = base64.b64encode(image_png)
        return f"Chart created: data:image/png;base64,{graphic.decode()}"
        
    except Exception as e:
        return f"Chart creation failed: {str(e)}"
```

### Tool Testing Suite

```python
class ToolTestSuite:
    def __init__(self, tool):
        self.tool = tool
        self.test_results = []
    
    def run_basic_tests(self):
        """Run basic functionality tests."""
        # Test valid inputs
        try:
            result = self.tool._run("test_input")
            self.test_results.append(("basic_functionality", "PASS", result))
        except Exception as e:
            self.test_results.append(("basic_functionality", "FAIL", str(e)))
    
    def run_error_tests(self):
        """Test error handling."""
        error_inputs = ["", None, "invalid_input", "extremely_long_input" * 1000]
        
        for error_input in error_inputs:
            try:
                result = self.tool._run(error_input)
                if "error" in result.lower():
                    self.test_results.append((f"error_handling_{error_input}", "PASS", result))
                else:
                    self.test_results.append((f"error_handling_{error_input}", "FAIL", "No error message"))
            except Exception as e:
                self.test_results.append((f"error_handling_{error_input}", "PASS", f"Exception caught: {str(e)}"))
    
    def generate_report(self):
        """Generate test report."""
        passed = len([r for r in self.test_results if r[1] == "PASS"])
        total = len(self.test_results)
        
        report = f"Tool Test Report: {self.tool.name}\n"
        report += f"Passed: {passed}/{total}\n\n"
        
        for test_name, status, details in self.test_results:
            report += f"{test_name}: {status}\n"
            if status == "FAIL":
                report += f"  Details: {details}\n"
        
        return report
```

### Documentation Template

```python
"""
Tool Name: [Tool Name]
Description: [Brief description of what the tool does]

Author: [Author name]
Version: [Version number]
Created: [Creation date]
Updated: [Last update date]

Dependencies:
- [List of required packages]

Environment Variables:
- [List of required environment variables]

Usage Examples:
```python
# Example 1: Basic usage
result = tool._run("example_input")

# Example 2: Advanced usage
result = tool._run("input", parameter="value")
```

Input Schema:
- parameter1 (str): Description of parameter1
- parameter2 (int, optional): Description of parameter2

Output Format:
- Returns string containing [description of output]

Error Handling:
- Returns error message string if operation fails
- Common errors: [list common error scenarios]

Security Considerations:
- [List security considerations]
- [Input validation measures]
- [Required permissions]

Performance Notes:
- Expected execution time: [time range]
- Memory usage: [memory requirements]
- Rate limits: [if applicable]

Testing:
```python
# Unit test example
def test_tool():
    tool = ToolClass()
    result = tool._run("test_input")
    assert "expected" in result
```
"""
```

---

*This comprehensive guide covers all aspects of AI agent tools development, from basic concepts to enterprise-grade implementations. Always test thoroughly and follow security best practices when deploying tools in production environments.*