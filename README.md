# Hivemind - Discord Server Management Bot

Hivemind is a powerful Discord bot designed for remote server management and monitoring through Discord. It allows authorized users to execute system commands, monitor system resources, and manage server operations directly from Discord.

## Features

- **Terminal Access**: Secure terminal access with user authentication
- **System Monitoring**: Real-time system information (CPU, Memory, Disk usage)
- **File Management**: List and manage files through Discord commands
- **Git Integration**: Pull repository updates directly through Discord
- **Logging System**: Comprehensive logging of all actions and commands
- **User Management**: Secure registration system for terminal access

## Installation

1. Clone the repository:
  ```bash
      git clone https://github.com/xxlyitemxx/hivemind.git
  ```
2. Install required dependencies:
   ```bash
       pip install -r requirements.txt
   ```
3. Create a `config.json` file
   ```json
     {
      "token": "YOUR_DISCORD_BOT_TOKEN",
      "owner_id": "YOUR_DISCORD_USER_ID",
      "registration_key": "YOUR_REGISTRATION_KEY",
      "log_key": "YOUR_LOG_ACCESS_KEY"
      }
   ```

## Configuration

- `token`: Your Discord bot token from the Discord Developer Portal
- `owner_id`: Your Discord user ID (required for admin commands)
- `registration_key`: Secret key for registering new terminal users
- `log_key`: Secret key for accessing bot logs

## Commands

- `!terminal` - Access the terminal interface (owner only)
- `!sysinfo` - Display system information
- `!register` - Register new terminal users (owner only)
- `!logs` - View bot logs (requires log access key)

## Security Features

- Secure user authentication system
- Encrypted password storage
- Session management for terminal access
- Role-based command access
- Comprehensive action logging

## Development

The project structure is organized as follows:
hivemind/
├── src/
│ ├── main.py
│ ├── command/
│ │ ├── ls.py
│ │ ├── pull.py
│ │ ├── system_info.py
│ │ ├── terminal.py
│ │ ├── register.py
│ │ └── logs.py
│ └── assets/
│ └── utils/
│ ├── config_loader.py
│ ├── credential_manager.py
│ ├── session_manager.py
│ └── logger.py
├── config.json
└── credentials.json

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Security Notice

⚠️ **Important**: Never share your config.json file or expose your bot token, registration key, or log key. These should be kept secure and private at all times.

## Support

For support, please open an issue in the GitHub repository or contact the maintainers directly.

---

Made with ❤️ by XxlyitemXx
