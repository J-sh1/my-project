import React, { useEffect } from 'react'
import { useParams } from 'react-router-dom'

const PostList = () => {

    // 페이징 처리, 게시글 목록 불러오기, 검색 이정도면 될듯?
  
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