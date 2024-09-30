import React, { useEffect } from 'react'
import { useParams } from 'react-router-dom'

const PostList = () => {
    const {category} = useParams()
    // console.log(category)

    useEffect(() => {

    }, [])

  return (
    <div>
        {category}
    </div>
  )
}

export default PostList