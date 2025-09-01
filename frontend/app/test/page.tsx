'use client'

import { useState, useEffect } from 'react'

export default function TestPage() {
  const [data, setData] = useState<any>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchData = async () => {
      try {
        console.log('Testing API call...')
        const response = await fetch('http://localhost:8001/habits')
        console.log('Response status:', response.status)
        const result = await response.json()
        console.log('Response data:', result)
        setData(result)
      } catch (err) {
        console.error('Error:', err)
        setError(err instanceof Error ? err.message : 'Unknown error')
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, [])

  if (loading) {
    return <div>Loading...</div>
  }

  if (error) {
    return <div>Error: {error}</div>
  }

  return (
    <div>
      <h1>API Test</h1>
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </div>
  )
}
