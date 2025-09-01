#!/usr/bin/env node
/**
 * Dynamic port assignment for Next.js frontend
 * Automatically finds available ports and starts the development server
 */

const { spawn } = require('child_process');
const net = require('net');

/**
 * Find a free port automatically
 * @returns {Promise<number>} Available port number
 */
function findFreePort() {
  return new Promise((resolve, reject) => {
    const server = net.createServer();
    
    server.listen(0, () => {
      const port = server.address().port;
      server.close(() => {
        resolve(port);
      });
    });
    
    server.on('error', reject);
  });
}

/**
 * Start Next.js with dynamic port
 */
async function startDynamic() {
  try {
    console.log('🚀 Starting Habit Loop Frontend with Dynamic Port...');
    
    // Find a free port
    const port = await findFreePort();
    
    console.log(`📡 Frontend running on: http://localhost:${port}`);
    console.log(`🎨 Development server: http://localhost:${port}`);
    console.log('=' * 60);
    
    // Start Next.js with the dynamic port
    const nextProcess = spawn('npx', ['next', 'dev', '-p', port.toString()], {
      stdio: 'inherit',
      shell: true
    });
    
    // Handle process termination
    process.on('SIGINT', () => {
      console.log('\n🛑 Shutting down frontend server...');
      nextProcess.kill('SIGINT');
      process.exit(0);
    });
    
    process.on('SIGTERM', () => {
      nextProcess.kill('SIGTERM');
      process.exit(0);
    });
    
  } catch (error) {
    console.error('❌ Error starting frontend:', error);
    process.exit(1);
  }
}

// Start the application
startDynamic();
