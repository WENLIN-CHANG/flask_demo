document.addEventListener('DOMContentLoaded', function() {
  console.log('Flask Demo 頁面載入完成！');

  // 為所有外部連結添加提示
  const links = document.querySelectorAll('a[href^="http"]');
  links.forEach(link => {
    link.addEventListener('click', function(event) {
      if (!confirm('確定要離開本網站嗎？')) {
        event.preventDefault();
      }
    });
  });
});