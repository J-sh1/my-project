import React from 'react'
import {Link} from 'react-router-dom'

const Header = () => {
  return (
    <div>
        <Link to={'/'}>
            <span className='nav-free-post'>자유게시판</span>
        </Link>

    </div>
  )
}

export default Header