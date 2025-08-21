'use client'

import { useState, useMemo } from 'react'
import { motion } from 'framer-motion'
import {
  useReactTable,
  getCoreRowModel,
  getPaginationRowModel,
  getSortedRowModel,
  getFilteredRowModel,
  flexRender,
  createColumnHelper,
  SortingState,
  ColumnFiltersState,
} from '@tanstack/react-table'
import { 
  ChevronLeft, 
  ChevronRight, 
  ChevronsLeft, 
  ChevronsRight,
  ArrowUpDown,
  ArrowUp,
  ArrowDown,
  Code,
  Info,
  Download,
  Search
} from 'lucide-react'

interface QueryResult {
  originalQuery: string
  generatedSQL: string
  explanation: string
  confidence: number
  results: any[]
  resultCount: number
}

interface ResultsTableProps {
  result: QueryResult
}

export default function ResultsTable({ result }: ResultsTableProps) {
  const [sorting, setSorting] = useState<SortingState>([])
  const [columnFilters, setColumnFilters] = useState<ColumnFiltersState>([])
  const [globalFilter, setGlobalFilter] = useState('')
  const [showSQL, setShowSQL] = useState(false)

  // Create columns dynamically based on the data
  const columns = useMemo(() => {
    if (!result.results || result.results.length === 0) return []
    
    const columnHelper = createColumnHelper<any>()
    const firstRow = result.results[0]
    
    return Object.keys(firstRow).map((key) =>
      columnHelper.accessor(key, {
        header: key,
        cell: (info) => {
          const value = info.getValue()
          if (value === null || value === undefined) {
            return <span className="text-gray-400 italic">null</span>
          }
          if (typeof value === 'boolean') {
            return <span className={value ? 'text-green-600' : 'text-red-600'}>{String(value)}</span>
          }
          if (typeof value === 'number') {
            return <span className="font-mono">{value.toLocaleString()}</span>
          }
          if (value instanceof Date) {
            return <span className="font-mono">{value.toLocaleDateString()}</span>
          }
          return <span className="max-w-xs truncate block" title={String(value)}>{String(value)}</span>
        },
      })
    )
  }, [result.results])

  const table = useReactTable({
    data: result.results,
    columns,
    state: {
      sorting,
      columnFilters,
      globalFilter,
    },
    onSortingChange: setSorting,
    onColumnFiltersChange: setColumnFilters,
    onGlobalFilterChange: setGlobalFilter,
    getCoreRowModel: getCoreRowModel(),
    getPaginationRowModel: getPaginationRowModel(),
    getSortedRowModel: getSortedRowModel(),
    getFilteredRowModel: getFilteredRowModel(),
    initialState: {
      pagination: {
        pageSize: 10,
      },
    },
  })

  const exportToCSV = () => {
    if (!result.results || result.results.length === 0) return
    
    const headers = Object.keys(result.results[0])
    const csvContent = [
      headers.join(','),
      ...result.results.map(row => 
        headers.map(header => {
          const value = row[header]
          return typeof value === 'string' ? `"${value.replace(/"/g, '""')}"` : value
        }).join(',')
      )
    ].join('\n')
    
    const blob = new Blob([csvContent], { type: 'text/csv' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'query-results.csv'
    a.click()
    URL.revokeObjectURL(url)
  }

  if (!result.results || result.results.length === 0) {
    return (
      <motion.div
        className="text-center py-12"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
      >
        <Search className="w-16 h-16 text-gray-400 mx-auto mb-4" />
        <h3 className="text-xl font-medium text-gray-900 mb-2">No results found</h3>
        <p className="text-gray-600">Your query executed successfully but returned no data.</p>
      </motion.div>
    )
  }

  return (
    <motion.div
      className="space-y-6"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      {/* Query Info */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <div className="flex items-start justify-between mb-4">
          <div className="flex-1">
            <h3 className="text-lg font-semibold text-gray-900 mb-2">Query Results</h3>
            <p className="text-gray-600 mb-3">"{result.originalQuery}"</p>
            <div className="flex items-center space-x-4 text-sm text-gray-500">
              <span>{result.resultCount} rows returned</span>
              <span>•</span>
              <span>Confidence: {Math.round(result.confidence * 100)}%</span>
            </div>
          </div>
          <div className="flex space-x-2">
            <button
              onClick={() => setShowSQL(!showSQL)}
              className="btn-secondary flex items-center space-x-2"
            >
              <Code className="w-4 h-4" />
              <span>{showSQL ? 'Hide' : 'Show'} SQL</span>
            </button>
            <button
              onClick={exportToCSV}
              className="btn-primary flex items-center space-x-2"
            >
              <Download className="w-4 h-4" />
              <span>Export CSV</span>
            </button>
          </div>
        </div>

        {/* SQL Display */}
        {showSQL && (
          <motion.div
            className="mt-4 p-4 bg-gray-50 rounded-lg border"
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
          >
            <div className="flex items-center mb-2">
              <Code className="w-4 h-4 text-gray-600 mr-2" />
              <span className="font-medium text-gray-900">Generated SQL:</span>
            </div>
            <pre className="text-sm text-gray-800 font-mono bg-white p-3 rounded border overflow-x-auto">
              {result.generatedSQL}
            </pre>
            <div className="mt-3 flex items-start">
              <Info className="w-4 h-4 text-blue-600 mr-2 mt-0.5 flex-shrink-0" />
              <p className="text-sm text-gray-700">{result.explanation}</p>
            </div>
          </motion.div>
        )}
      </div>

      {/* Table Controls */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <div className="relative">
              <Search className="w-4 h-4 absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
              <input
                value={globalFilter ?? ''}
                onChange={(e) => setGlobalFilter(e.target.value)}
                placeholder="Search all columns..."
                className="pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
              />
            </div>
          </div>
          <div className="text-sm text-gray-600">
            Showing {table.getRowModel().rows.length} of {result.resultCount} rows
          </div>
        </div>
      </div>

      {/* Data Table */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gray-50 border-b border-gray-200">
              {table.getHeaderGroups().map((headerGroup) => (
                <tr key={headerGroup.id}>
                  {headerGroup.headers.map((header) => (
                    <th
                      key={header.id}
                      className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100 transition-colors"
                      onClick={header.column.getToggleSortingHandler()}
                    >
                      <div className="flex items-center space-x-1">
                        <span>
                          {flexRender(header.column.columnDef.header, header.getContext())}
                        </span>
                        <span className="text-gray-400">
                          {{
                            asc: <ArrowUp className="w-4 h-4" />,
                            desc: <ArrowDown className="w-4 h-4" />,
                          }[header.column.getIsSorted() as string] ?? (
                            <ArrowUpDown className="w-4 h-4" />
                          )}
                        </span>
                      </div>
                    </th>
                  ))}
                </tr>
              ))}
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {table.getRowModel().rows.map((row, index) => (
                <motion.tr
                  key={row.id}
                  className="hover:bg-gray-50 transition-colors"
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.05 }}
                >
                  {row.getVisibleCells().map((cell) => (
                    <td key={cell.id} className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {flexRender(cell.column.columnDef.cell, cell.getContext())}
                    </td>
                  ))}
                </motion.tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Pagination */}
        <div className="bg-gray-50 px-6 py-3 border-t border-gray-200">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <span className="text-sm text-gray-700">
                Page {table.getState().pagination.pageIndex + 1} of {table.getPageCount()}
              </span>
              <select
                value={table.getState().pagination.pageSize}
                onChange={(e) => table.setPageSize(Number(e.target.value))}
                className="border border-gray-300 rounded px-2 py-1 text-sm"
              >
                {[10, 20, 50, 100].map((pageSize) => (
                  <option key={pageSize} value={pageSize}>
                    Show {pageSize}
                  </option>
                ))}
              </select>
            </div>

            <div className="flex items-center space-x-2">
              <button
                onClick={() => table.setPageIndex(0)}
                disabled={!table.getCanPreviousPage()}
                className="p-2 border border-gray-300 rounded hover:bg-gray-100 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <ChevronsLeft className="w-4 h-4" />
              </button>
              <button
                onClick={() => table.previousPage()}
                disabled={!table.getCanPreviousPage()}
                className="p-2 border border-gray-300 rounded hover:bg-gray-100 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <ChevronLeft className="w-4 h-4" />
              </button>
              <button
                onClick={() => table.nextPage()}
                disabled={!table.getCanNextPage()}
                className="p-2 border border-gray-300 rounded hover:bg-gray-100 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <ChevronRight className="w-4 h-4" />
              </button>
              <button
                onClick={() => table.setPageIndex(table.getPageCount() - 1)}
                disabled={!table.getCanNextPage()}
                className="p-2 border border-gray-300 rounded hover:bg-gray-100 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <ChevronsRight className="w-4 h-4" />
              </button>
            </div>
          </div>
        </div>
      </div>
    </motion.div>
  )
}
