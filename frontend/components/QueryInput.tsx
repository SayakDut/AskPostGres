'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'
import { Send, Sparkles } from 'lucide-react'

interface QueryInputProps {
  onSubmit: (query: string) => void
  isLoading: boolean
}

const exampleQueries = [
  "Show me all users who registered this month",
  "What are the top 10 best-selling products?",
  "Find customers with orders over $1000",
  "Show me the average order value by month",
]

export default function QueryInput({ onSubmit, isLoading }: QueryInputProps) {
  const [query, setQuery] = useState('')

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (query.trim() && !isLoading) {
      onSubmit(query.trim())
    }
  }

  const handleExampleClick = (example: string) => {
    setQuery(example)
  }

  return (
    <div className="w-full max-w-4xl mx-auto">
      {/* Main Input Form */}
      <form onSubmit={handleSubmit} className="relative">
        <div className="relative">
          <textarea
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Ask a question about your data... (e.g., 'Show me all users who signed up last week')"
            className="w-full px-6 py-4 pr-16 text-lg border-2 border-gray-200 rounded-2xl focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-all duration-200 bg-white shadow-sm resize-none"
            rows={3}
            maxLength={1000}
            disabled={isLoading}
          />
          
          {/* Submit Button */}
          <motion.button
            type="submit"
            disabled={!query.trim() || isLoading}
            className="absolute bottom-4 right-4 p-3 bg-primary-600 text-white rounded-xl hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            {isLoading ? (
              <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
            ) : (
              <Send className="w-5 h-5" />
            )}
          </motion.button>
        </div>
        
        {/* Character Count */}
        <div className="flex justify-between items-center mt-2 px-2">
          <span className="text-sm text-gray-500">
            {query.length}/1000 characters
          </span>
          {query.trim() && (
            <motion.span 
              className="text-sm text-primary-600 font-medium"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
            >
              Press Enter + Ctrl to submit
            </motion.span>
          )}
        </div>
      </form>

      {/* Example Queries */}
      <motion.div 
        className="mt-6"
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3 }}
      >
        <div className="flex items-center mb-3">
          <Sparkles className="w-4 h-4 text-primary-600 mr-2" />
          <span className="text-sm font-medium text-gray-700">Try these examples:</span>
        </div>
        
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
          {exampleQueries.map((example, index) => (
            <motion.button
              key={index}
              onClick={() => handleExampleClick(example)}
              className="text-left p-3 text-sm text-gray-600 bg-gray-50 hover:bg-gray-100 rounded-lg transition-colors duration-200 border border-gray-200 hover:border-gray-300"
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              disabled={isLoading}
            >
              "{example}"
            </motion.button>
          ))}
        </div>
      </motion.div>
    </div>
  )
}
