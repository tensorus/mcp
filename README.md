---
license: mit
title: Tensorus MCP
sdk: python
emoji: 🐠
colorFrom: blue
colorTo: yellow
short_description: Model Context Protocol server and client for Tensorus tensor database
---

# Tensorus MCP

Model Context Protocol (MCP) server and client for Tensorus tensor database operations. This package provides a standardized interface for AI agents and LLMs to interact with Tensorus capabilities using the Model Context Protocol.

## Features

- **MCP Server**: Python implementation using `fastmcp` for tensor database operations
- **MCP Client**: Python client library for easy integration with MCP servers
- **Tensor Operations**: Complete set of tensor manipulation tools via MCP
- **Dataset Management**: Create, list, and manage tensor datasets
- **Demo Mode**: Pre-configured mock data for testing and demonstration

## Installation

```bash
pip install fastmcp
pip install -r requirements.txt
```

## Quick Start

### Starting the MCP Server

```bash
python -m tensorus_mcp.server
```

For web endpoint support:
```bash
python -m tensorus_mcp.server --transport streamable-http
```

### Demo Mode

For demonstration or testing purposes, run the server in demo mode:

```bash
python -m tensorus_mcp.server --demo-mode
```

### Using the Python Client

```python
from tensorus_mcp.client import TensorusMCPClient

async def example():
    async with TensorusMCPClient.from_http("http://localhost:8000/mcp/") as client:
        # List available datasets
        datasets = await client.list_datasets()
        print(f"Available datasets: {datasets}")
        
        # Create a new dataset
        await client.create_dataset("my_dataset")
        
        # Ingest a tensor
        result = await client.ingest_tensor(
            dataset_name="my_dataset",
            tensor_shape=[2, 2],
            tensor_dtype="float32",
            tensor_data=[[1.0, 2.0], [3.0, 4.0]],
            metadata={"source": "example"}
        )
        print(f"Ingested tensor with ID: {result['record_id']}")
```

## MCP Demo Script

### Prerequisites

* Tensorus MCP Server running (`python -m tensorus_mcp.server`)
* For live mode: Tensorus backend API accessible
* For demo mode: No additional setup required

### Demo Scenario: MCP Client Interaction

**Goal:** Demonstrate how an external AI agent can leverage Tensorus via MCP.

1. **Start MCP Server:**
   ```bash
   python -m tensorus_mcp.server --demo-mode
   ```

2. **Connect via Python Client:**
   ```python
   from tensorus_mcp.client import TensorusMCPClient
   
   async def demo():
       async with TensorusMCPClient.from_http("http://localhost:8000/mcp/") as client:
           # List available datasets
           datasets = await client.list_datasets()
           print(f"Available datasets: {datasets}")
           
           # Create a new dataset
           result = await client.create_dataset("demo_dataset")
           print(f"Created dataset: {result}")
           
           # Ingest sample tensor data
           tensor_result = await client.ingest_tensor(
               dataset_name="demo_dataset",
               tensor_shape=[3, 3],
               tensor_dtype="float32",
               tensor_data=[[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]],
               metadata={"source": "mcp_demo", "type": "sample_matrix"}
           )
           print(f"Ingested tensor: {tensor_result}")
           
           # Apply tensor operation (transpose)
           op_result = await client.apply_operation(
               operation="transpose",
               dataset_name="demo_dataset",
               record_id=tensor_result["record_id"],
               dim0=0,
               dim1=1
           )
           print(f"Applied transpose operation: {op_result}")
   ```

3. **Conceptual Client Interaction (JavaScript):**
   ```javascript
   // Example of how other AI agents could interact via MCP
   async function mcpDemo() {
       // List available tools
       const { tools } = await client.request({ method: 'tools/list' }, {});
       console.log("Available Tensorus Tools:", tools.map(t => t.name));
       
       // Create dataset via MCP
       const createResponse = await client.request({ method: 'tools/call' }, {
           name: 'tensorus_create_dataset',
           arguments: { dataset_name: 'mcp_demo_dataset' }
       });
       console.log("Dataset created:", createResponse.content[0].text);
       
       // Ingest tensor via MCP
       const ingestResponse = await client.request({ method: 'tools/call' }, {
           name: 'tensorus_ingest_tensor',
           arguments: {
               dataset_name: 'mcp_demo_dataset',
               tensor_shape: [2, 2],
               tensor_dtype: 'float32',
               tensor_data: [[1.0, 2.0], [3.0, 4.0]],
               metadata: { source: 'mcp_demo' }
           }
       });
       console.log("Tensor ingested:", ingestResponse.content[0].text);
   }
   ```

## Available MCP Tools

### Dataset Management
- `tensorus_list_datasets`: Lists all available datasets
- `tensorus_create_dataset`: Creates a new dataset
- `tensorus_delete_dataset`: Deletes an existing dataset

### Tensor Operations
- `tensorus_ingest_tensor`: Ingests a new tensor into a dataset
- `tensorus_get_tensor_details`: Retrieves tensor data and metadata
- `tensorus_delete_tensor`: Deletes a specific tensor
- `tensorus_update_tensor_metadata`: Updates tensor metadata

### Tensor Computations
- `tensorus_apply_unary_operation`: Operations like `log`, `reshape`, `transpose`, `sum`, `mean`
- `tensorus_apply_binary_operation`: Operations like `add`, `subtract`, `multiply`, `matmul`
- `tensorus_apply_list_operation`: Operations like `concatenate` and `stack`
- `tensorus_apply_einsum`: Einstein summation operations

### Diagnostic Tools
- `mcp_server_status`: Check server operational status
- `connection_test`: Lightweight connectivity check
- `backend_ping`: Test backend API health endpoint
- `backend_connectivity_test`: Verify backend communication

## Configuration

### API Key Management

When not in demo mode, provide authentication via:

1. **Global API Key**: Set when starting the server
   ```bash
   python -m tensorus_mcp.server --mcp-api-key YOUR_API_KEY
   ```

2. **Per-Tool API Key**: Pass `api_key` parameter in tool calls

### Environment Variables

- `TENSORUS_API_BASE_URL`: Backend API URL (default: `https://tensorus-core.hf.space`)
- `TENSORUS_MINIMAL_IMPORT`: Set to `1` for lightweight imports

## Demo Examples

### Interactive Notebook
See `examples/demo_notebook.ipynb` for a complete interactive example.

### Streamlit App
Launch the demo Streamlit app:
```bash
streamlit run examples/demo_app.py
```

## Development

### Running Tests

```bash
# Install test dependencies
pip install -r examples/requirements.txt

# Run MCP-specific tests
pytest tests/test_mcp_integration.py
```

### Project Structure

```
tensorus_mcp/
├── __init__.py          # Package initialization
├── server.py            # MCP server implementation
├── client.py            # MCP client library
└── config.py            # Configuration management

examples/
├── demo_app.py          # Streamlit demo application
├── demo_notebook.ipynb  # Interactive Jupyter notebook
└── requirements.txt     # Demo dependencies

tests/
└── test_mcp_integration.py  # Integration tests
```

## Usage in Claude Desktop

Add to your Claude Desktop MCP settings:

```json
{
  "mcpServers": {
    "tensorus": {
      "command": "python",
      "args": ["-m", "tensorus_mcp.server"],
      "env": {
        "TENSORUS_API_BASE_URL": "https://tensorus-core.hf.space"
      }
    }
  }
}
```

## API Reference

### TensorusMCPClient Methods

- `list_datasets()`: Get all available datasets
- `create_dataset(name, schema=None)`: Create a new dataset
- `ingest_tensor(dataset_name, tensor_shape, tensor_dtype, tensor_data, metadata)`: Add tensor to dataset
- `get_tensor_details(dataset_name, record_id)`: Retrieve tensor information
- `apply_operation(operation, dataset_name, record_id, **kwargs)`: Apply tensor operations

## Contributing

Contributions are welcome! Please feel free to open issues or submit pull requests.

## License

MIT License