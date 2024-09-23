import axios from "axios"

// axios 인스턴스 생성
const instance = axios.create({
    headers: {
        'X-CSRFToken': getCsrfTokenFromCookies(),  // 쿠키에서 가져온 CSRF 토큰 함수
    },
    withCredentials: true  // 쿠키와 함께 요청 전송
});

// 쿠키에서 CSRF 토큰을 가져오는 함수
function getCsrfTokenFromCookies() {
    const csrfCookie = document.cookie
      .split('; ')
      .find(row => row.startsWith('csrf_token='));
    return csrfCookie ? csrfCookie.split('=')[1] : '';
  }  

export default instance
