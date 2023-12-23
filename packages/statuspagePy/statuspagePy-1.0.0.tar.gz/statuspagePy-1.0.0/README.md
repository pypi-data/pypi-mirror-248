# Atlassian Statuspage API: Python Implementation

## Overview

This project provides a comprehensive Python implementation of the Atlassian Statuspage OpenAPI interface. It is designed to seamlessly integrate with existing Python applications and systems, offering a straightforward and efficient way to interact with Atlassian Statuspage services.

## Key Features

- **Complete API Coverage**: Implements all the functionalities of the Atlassian Statuspage OpenAPI, ensuring comprehensive control and management of status pages.
- **Pythonic Design**: The implementation is designed with Python idioms and practices in mind, making it intuitive for Python developers.
- **Ease of Integration**: Easily integrates into existing Python codebases, facilitating smooth adoption and transition.
- **Efficient Error Handling**: Robust error handling mechanisms provide clear and actionable feedback for effective troubleshooting.
- **Comprehensive Documentation**: Detailed documentation and examples to help users quickly understand and leverage the API's capabilities.

## Getting Started

To begin using this Python implementation in your project, simply clone the repository and install the necessary dependencies:

```bash
git clone https://github.com/dielect/PyStatusPage.git
pip install -r requirements.txt
```
## Initialization Parameters

When initializing the `StatusPageAPI`, the following parameters control its behavior:

| Parameter     | Type    | Requirement  | Description |
|---------------|---------|--------------|-------------|
| `api_key`     | `str`   | Mandatory    | Your API key for accessing Atlassian Statuspage. |
| `raw_response`| `bool`  | Optional     | Determines the type of response returned by the API methods. If set to `True`, methods return the complete HTTP `Response` object, providing access to details like status codes and headers. By default (`False`), methods return the parsed JSON data. |

### Example Usage

```python
from statuspagePyAPI.statuspage_api import StatusPageAPI

# Initializing with raw_response as True
api = StatusPageAPI(api_key='YOUR_API_KEY', raw_response=True)

# Example API call
response = api.components.get_components(page_id='YOUR_PAGE_ID')

# Accessing the response
if response.raw_response:
    print("Status Code:", response.status_code)
    print("JSON Data:", response.json())
else:
    print("Data:", response)
```

## Roadmap

- [x] Complete development of components module.
- [ ] Add asynchronous support for concurrent API calls.
- [ ] Implement caching mechanisms for improved performance.
- [ ] Expand the suite of integration tests for better coverage.


## Contributing

Contributions are welcome! Whether it's submitting bugs, suggesting new features, or improving documentation, your help is appreciated. Please refer to the [CONTRIBUTING.md](CONTRIBUTING.md) file for contribution guidelines.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For any queries or feedback, please reach out to me at dielectric.army@gmail.com.

