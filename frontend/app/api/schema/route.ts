import { NextResponse } from 'next/server'
import { getDatabaseSchema } from '@/lib/schema'
import { testConnection } from '@/lib/database'

export async function GET() {
  try {
    // Test database connection
    const isConnected = await testConnection()
    if (!isConnected) {
      return NextResponse.json(
        { error: 'Database connection failed. Please check your configuration.' },
        { status: 500 }
      )
    }

    // Get database schema
    const schema = await getDatabaseSchema()

    return NextResponse.json({
      success: true,
      data: {
        tables: schema,
        tableCount: schema.length,
        totalColumns: schema.reduce((sum, table) => sum + table.columns.length, 0)
      }
    })

  } catch (error: any) {
    console.error('Schema API Error:', error)

    if (error.code === 'ECONNREFUSED') {
      return NextResponse.json(
        { error: 'Cannot connect to the database. Please check your database configuration.' },
        { status: 500 }
      )
    }

    return NextResponse.json(
      { error: 'Failed to retrieve database schema.' },
      { status: 500 }
    )
  }
}
