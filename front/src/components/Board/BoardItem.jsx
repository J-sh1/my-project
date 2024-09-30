import React, { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'

const BoardItem = ({category}) => {

    const [board, setBoard] = useState('')

    useEffect(() => {
        if (category == 'free'){
            setBoard('자유')
        } else if (category == 'news') {
            setBoard('기사')
        } else if (category == 'question') {
            setBoard('질문')
        } else if (category == 'test') {
            setBoard('임시')
        }
    }, [])

  return (
    <div className="content-row">
        <span>{board}</span>
        <Link to = {'/login'}>게시판테스트1</Link>
        <span>10</span>
    </div>
  )
}

export default BoardItem