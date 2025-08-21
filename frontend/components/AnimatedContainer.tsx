'use client'

import { motion, AnimatePresence } from 'framer-motion'
import { ReactNode } from 'react'

interface AnimatedContainerProps {
  children: ReactNode
  className?: string
  delay?: number
  duration?: number
  direction?: 'up' | 'down' | 'left' | 'right'
  stagger?: boolean
}

const directionVariants = {
  up: { y: 20, opacity: 0 },
  down: { y: -20, opacity: 0 },
  left: { x: 20, opacity: 0 },
  right: { x: -20, opacity: 0 },
}

export default function AnimatedContainer({
  children,
  className = '',
  delay = 0,
  duration = 0.5,
  direction = 'up',
  stagger = false,
}: AnimatedContainerProps) {
  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        duration,
        delay,
        staggerChildren: stagger ? 0.1 : 0,
      },
    },
  }

  const itemVariants = {
    hidden: directionVariants[direction],
    visible: {
      x: 0,
      y: 0,
      opacity: 1,
      transition: {
        duration,
        ease: 'easeOut',
      },
    },
  }

  return (
    <motion.div
      className={className}
      variants={containerVariants}
      initial="hidden"
      animate="visible"
    >
      {stagger ? (
        Array.isArray(children) ? (
          children.map((child, index) => (
            <motion.div key={index} variants={itemVariants}>
              {child}
            </motion.div>
          ))
        ) : (
          <motion.div variants={itemVariants}>{children}</motion.div>
        )
      ) : (
        <motion.div variants={itemVariants}>{children}</motion.div>
      )}
    </motion.div>
  )
}
