import React, { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'

const BoardItem = ({category, title, date, link}) => {

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
        <Link to = {link} target="_blank">{title}</Link>
        <span>{date}</span>
    </div>
  )
}

export default BoardItem