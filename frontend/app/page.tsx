'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'
import { Search, Database, Sparkles, AlertCircle } from 'lucide-react'
import QueryInput from '@/components/QueryInput'
import ResultsTable from '@/components/ResultsTable'
import LoadingSpinner from '@/components/LoadingSpinner'
import ErrorMessage from '@/components/ErrorMessage'
import { ToastContainer } from '@/components/Toast'
import { useToast } from '@/hooks/useToast'
import { api, QueryResult } from '@/lib/api'

export default function HomePage() {
  const [isLoading, setIsLoading] = useState(false)
  const [result, setResult] = useState<QueryResult | null>(null)
  const [error, setError] = useState<string | null>(null)
  const { toasts, removeToast, success, error: showError } = useToast()

  const handleQuery = async (query: string) => {
    setIsLoading(true)
    setError(null)
    setResult(null)

    try {
      const result = await api.executeQuery(query)
      setResult(result)
      success('Query executed successfully!', `Found ${result.result_count} results`)
    } catch (err: any) {
      setError(err.message || 'An unexpected error occurred')
      showError('Query failed', err.message || 'An unexpected error occurred')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
      {/* Header */}
      <motion.header 
        className="bg-white shadow-sm border-b border-gray-200"
        initial={{ y: -20, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ duration: 0.5 }}
      >
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center space-x-3">
            <div className="flex items-center justify-center w-12 h-12 bg-primary-600 rounded-xl">
              <Database className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-3xl font-bold text-gray-900">AskPostgres</h1>
              <p className="text-gray-600">Query your database with natural language</p>
            </div>
          </div>
        </div>
      </motion.header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Hero Section */}
        <motion.div 
          className="text-center mb-12"
          initial={{ y: 20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ duration: 0.5, delay: 0.2 }}
        >
          <div className="flex items-center justify-center mb-4">
            <Sparkles className="w-8 h-8 text-primary-600 mr-2" />
            <h2 className="text-2xl font-semibold text-gray-900">
              Ask questions about your data
            </h2>
          </div>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            Type your question in plain English and get instant SQL results from your PostgreSQL database.
          </p>
        </motion.div>

        {/* Query Input */}
        <motion.div 
          className="mb-8"
          initial={{ y: 20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ duration: 0.5, delay: 0.4 }}
        >
          <QueryInput onSubmit={handleQuery} isLoading={isLoading} />
        </motion.div>

        {/* Loading State */}
        {isLoading && (
          <motion.div 
            className="flex justify-center mb-8"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
          >
            <LoadingSpinner />
          </motion.div>
        )}

        {/* Error State */}
        {error && (
          <motion.div 
            className="mb-8"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
          >
            <ErrorMessage message={error} />
          </motion.div>
        )}

        {/* Results */}
        {result && !isLoading && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
          >
            <ResultsTable result={result} />
          </motion.div>
        )}

        {/* Empty State */}
        {!result && !isLoading && !error && (
          <motion.div 
            className="text-center py-16"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.5, delay: 0.6 }}
          >
            <Search className="w-16 h-16 text-gray-400 mx-auto mb-4" />
            <h3 className="text-xl font-medium text-gray-900 mb-2">
              Ready to explore your data
            </h3>
            <p className="text-gray-600">
              Enter a question above to get started with natural language database queries.
            </p>
          </motion.div>
        )}
      </main>

      {/* Toast Notifications */}
      <ToastContainer toasts={toasts} onClose={removeToast} />
    </div>
  )
}
