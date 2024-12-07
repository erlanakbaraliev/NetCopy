**NetCopyEn**  
A client-server application for file transfer and data verification using CRC or MD5 checksums. Includes three components:  
1. **Checksum Server**: Stores and validates checksums with expiry.  
2. **NetCopy Client**: Sends files and associated checksums to the server.  
3. **NetCopy Server**: Receives files, retrieves checksums, and verifies file integrity.

### Features:  
- **Reliable File Transfer**: Uses TCP for byte-wise transmission.  
- **Checksum Validation**: Ensures file integrity with server-side verification.  
- **Dynamic Expiry**: Maintains checksum validity for a specified duration.

### How to Run:  
Follow the instructions in the README to configure and execute the components for seamless file transfer and validation.

