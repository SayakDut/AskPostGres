'use client'

import { motion } from 'framer-motion'
import { Database, Sparkles, Search } from 'lucide-react'

export default function LoadingSpinner() {
  return (
    <div className="flex flex-col items-center justify-center py-12">
      {/* Animated Icons */}
      <div className="relative mb-6">
        <motion.div
          className="flex items-center space-x-4"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.5 }}
        >
          <motion.div
            animate={{ 
              rotate: 360,
              scale: [1, 1.1, 1]
            }}
            transition={{ 
              rotate: { duration: 2, repeat: Infinity, ease: "linear" },
              scale: { duration: 1, repeat: Infinity, ease: "easeInOut" }
            }}
            className="p-3 bg-primary-100 rounded-full"
          >
            <Search className="w-6 h-6 text-primary-600" />
          </motion.div>
          
          <motion.div
            animate={{ 
              x: [0, 10, 0],
              opacity: [0.5, 1, 0.5]
            }}
            transition={{ 
              duration: 1.5, 
              repeat: Infinity, 
              ease: "easeInOut" 
            }}
            className="p-2 bg-yellow-100 rounded-full"
          >
            <Sparkles className="w-5 h-5 text-yellow-600" />
          </motion.div>
          
          <motion.div
            animate={{ 
              scale: [1, 1.2, 1],
              rotate: [0, 5, -5, 0]
            }}
            transition={{ 
              duration: 2, 
              repeat: Infinity, 
              ease: "easeInOut" 
            }}
            className="p-3 bg-green-100 rounded-full"
          >
            <Database className="w-6 h-6 text-green-600" />
          </motion.div>
        </motion.div>
      </div>

      {/* Loading Text */}
      <motion.div
        className="text-center"
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3 }}
      >
        <h3 className="text-lg font-semibold text-gray-900 mb-2">
          Processing your query...
        </h3>
        <p className="text-gray-600 max-w-md">
          Our AI is analyzing your question and generating the perfect SQL query for your database.
        </p>
      </motion.div>

      {/* Progress Steps */}
      <motion.div 
        className="mt-8 flex items-center space-x-4"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.6 }}
      >
        {['Understanding', 'Generating SQL', 'Executing'].map((step, index) => (
          <motion.div
            key={step}
            className="flex items-center"
            initial={{ opacity: 0.3 }}
            animate={{ opacity: 1 }}
            transition={{ 
              delay: index * 0.5,
              duration: 0.5,
              repeat: Infinity,
              repeatType: "reverse"
            }}
          >
            <div className="w-2 h-2 bg-primary-600 rounded-full mr-2" />
            <span className="text-sm text-gray-600">{step}</span>
            {index < 2 && (
              <motion.div 
                className="w-8 h-0.5 bg-gray-300 mx-3"
                animate={{ scaleX: [0, 1, 0] }}
                transition={{ 
                  duration: 1.5, 
                  repeat: Infinity,
                  delay: index * 0.3
                }}
              />
            )}
          </motion.div>
        ))}
      </motion.div>
    </div>
  )
}
