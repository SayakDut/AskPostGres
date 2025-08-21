import { NextResponse } from 'next/server'
import { testConnection } from '@/lib/database'
import { validateEnvironmentConfig } from '@/lib/security'

export async function GET() {
  try {
    // Check environment configuration
    const envValidation = validateEnvironmentConfig()
    if (!envValidation.isValid) {
      return NextResponse.json(
        { 
          status: 'error',
          message: 'Environment configuration invalid',
          errors: envValidation.errors
        },
        { status: 500 }
      )
    }

    // Test database connection
    const dbConnected = await testConnection()
    
    return NextResponse.json({
      status: 'healthy',
      timestamp: new Date().toISOString(),
      services: {
        database: dbConnected ? 'connected' : 'disconnected',
        environment: 'configured'
      }
    })

  } catch (error) {
    return NextResponse.json(
      { 
        status: 'error',
        message: 'Health check failed',
        timestamp: new Date().toISOString()
      },
      { status: 500 }
    )
  }
}
