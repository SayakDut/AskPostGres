'use client'

import { motion } from 'framer-motion'
import { AlertCircle, RefreshCw, Lightbulb } from 'lucide-react'

interface ErrorMessageProps {
  message: string
  onRetry?: () => void
}

const errorSuggestions = [
  "Try rephrasing your question more specifically",
  "Check if the table or column names exist in your database",
  "Make sure your database connection is working",
  "Use simpler language and avoid complex joins initially"
]

export default function ErrorMessage({ message, onRetry }: ErrorMessageProps) {
  return (
    <motion.div
      className="max-w-2xl mx-auto"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      transition={{ duration: 0.3 }}
    >
      <div className="bg-red-50 border border-red-200 rounded-xl p-6">
        {/* Error Header */}
        <div className="flex items-start space-x-3">
          <div className="flex-shrink-0">
            <AlertCircle className="w-6 h-6 text-red-600" />
          </div>
          <div className="flex-1">
            <h3 className="text-lg font-semibold text-red-900 mb-2">
              Oops! Something went wrong
            </h3>
            <p className="text-red-800 mb-4">
              {message}
            </p>

            {/* Retry Button */}
            {onRetry && (
              <motion.button
                onClick={onRetry}
                className="inline-flex items-center px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2"
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
              >
                <RefreshCw className="w-4 h-4 mr-2" />
                Try Again
              </motion.button>
            )}
          </div>
        </div>

        {/* Suggestions */}
        <motion.div 
          className="mt-6 pt-6 border-t border-red-200"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.2 }}
        >
          <div className="flex items-center mb-3">
            <Lightbulb className="w-5 h-5 text-red-600 mr-2" />
            <h4 className="font-medium text-red-900">Suggestions:</h4>
          </div>
          <ul className="space-y-2">
            {errorSuggestions.map((suggestion, index) => (
              <motion.li
                key={index}
                className="flex items-start text-sm text-red-800"
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.1 * index }}
              >
                <span className="w-1.5 h-1.5 bg-red-600 rounded-full mt-2 mr-3 flex-shrink-0" />
                {suggestion}
              </motion.li>
            ))}
          </ul>
        </motion.div>
      </div>
    </motion.div>
  )
}
