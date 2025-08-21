import { NextRequest, NextResponse } from 'next/server'
import { generateSQLFromNaturalLanguage } from '@/lib/llm'
import { executeReadOnlyQuery, testConnection } from '@/lib/database'
import { getDatabaseSchema } from '@/lib/schema'
import { validateSQLQuery, sanitizeUserInput, checkRateLimit } from '@/lib/security'

export async function POST(request: NextRequest) {
  try {
    // Rate limiting
    const clientIP = request.ip || request.headers.get('x-forwarded-for') || 'unknown'
    if (!checkRateLimit(clientIP)) {
      return NextResponse.json(
        { error: 'Too many requests. Please wait before trying again.' },
        { status: 429 }
      )
    }

    // Parse request body
    const body = await request.json()
    const { query } = body

    // Validate and sanitize input
    if (!query || typeof query !== 'string' || query.trim().length === 0) {
      return NextResponse.json(
        { error: 'Query is required and must be a non-empty string' },
        { status: 400 }
      )
    }

    const sanitizedQuery = sanitizeUserInput(query)
    if (!sanitizedQuery) {
      return NextResponse.json(
        { error: 'Invalid query format' },
        { status: 400 }
      )
    }

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
    if (schema.length === 0) {
      return NextResponse.json(
        { error: 'No tables found in the database.' },
        { status: 404 }
      )
    }

    // Generate SQL from natural language
    const llmResponse = await generateSQLFromNaturalLanguage(sanitizedQuery, schema)

    // Validate the generated SQL for security
    const validation = validateSQLQuery(llmResponse.sql)
    if (!validation.isValid) {
      return NextResponse.json(
        {
          error: 'Generated query failed security validation',
          details: validation.errors
        },
        { status: 400 }
      )
    }

    // Execute the validated SQL query
    const results = await executeReadOnlyQuery(validation.sanitizedQuery!)

    // Return successful response
    return NextResponse.json({
      success: true,
      data: {
        originalQuery: sanitizedQuery,
        generatedSQL: validation.sanitizedQuery,
        explanation: llmResponse.explanation,
        confidence: llmResponse.confidence,
        results: results,
        resultCount: results.length,
        warnings: validation.warnings
      }
    })

  } catch (error: any) {
    console.error('API Error:', error)

    // Handle specific error types
    if (error.message.includes('Only SELECT queries are allowed')) {
      return NextResponse.json(
        { error: 'Only read-only SELECT queries are allowed for security reasons.' },
        { status: 403 }
      )
    }

    if (error.message.includes('Failed to generate SQL query')) {
      return NextResponse.json(
        { error: 'Could not understand your query. Please try rephrasing it.' },
        { status: 400 }
      )
    }

    if (error.code === 'ECONNREFUSED') {
      return NextResponse.json(
        { error: 'Cannot connect to the database. Please check your database configuration.' },
        { status: 500 }
      )
    }

    // Generic error response
    return NextResponse.json(
      { error: 'An unexpected error occurred. Please try again.' },
      { status: 500 }
    )
  }
}
