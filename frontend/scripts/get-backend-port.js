#!/usr/bin/env node
/**
 * Get the current backend port from running processes
 */

const { exec } = require('child_process');
const { promisify } = require('util');

const execAsync = promisify(exec);

/**
 * Get the port of the running backend server
 * @returns {Promise<number>} Backend port number
 */
async function getBackendPort() {
  try {
    // Get all processes
    const { stdout } = await execAsync('ps aux');
    const lines = stdout.split('\n');
    
    for (const line of lines) {
      if (line.includes('uvicorn') && line.includes('app.main:app')) {
        // Extract port from command line
        const portMatch = line.match(/--port\s+(\d+)/);
        if (portMatch) {
          return parseInt(portMatch[1]);
        }
      }
    }
    
    // If no port found, return default
    return 8000;
  } catch (error) {
    console.error('Error getting backend port:', error);
    return 8000;
  }
}

/**
 * Main function
 */
async function main() {
  const port = await getBackendPort();
  console.log(port);
}

// Run if called directly
if (require.main === module) {
  main();
}

module.exports = { getBackendPort };
