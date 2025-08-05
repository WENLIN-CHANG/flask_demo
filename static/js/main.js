document.addEventListener('DOMContentLoaded', function() {
  // 為所有外部連結添加提示
  const links = document.querySelectorAll('a[href^="http"]');
  links.forEach(link => {
    link.addEventListener('click', function(event) {
      if (!confirm('確定要離開本網站嗎？')) {
        event.preventDefault();
      }
    });
  });

  // 頭像上傳功能
  const avatarForm = document.getElementById('avatar-form');
  const avatarInput = document.getElementById('avatar');
  const previewImage = document.getElementById('preview-image');
  const previewContainer = document.querySelector('.preview_container');
  const uploadProgress = document.getElementById('upload-progress');
  const uploadBtn = document.getElementById('upload-btn');
  const deleteBtn = document.getElementById('delete-btn');
  const currentAvatar = document.getElementById('current-avatar');

  // 只在頭像上傳頁面執行
  if (!avatarForm) return;

  // 圖片預覽功能
  if (avatarInput) {
    avatarInput.addEventListener('change', function(e) {
      const file = e.target.files[0];
      if (file) {
        // 檢查文件類型
        const allowedTypes = ['image/png', 'image/jpg', 'image/jpeg', 'image/gif', 'image/webp'];
        if (!allowedTypes.includes(file.type)) {
          alert('請選擇有效的圖片格式 (PNG, JPG, JPEG, GIF, WebP)');
          return;
        }

        // 檢查文件大小 (16MB)
        if (file.size > 16 * 1024 * 1024) {
          alert('檔案大小不能超過 16MB');
          return;
        }

        // 顯示預覽
        const reader = new FileReader();
        reader.onload = function(e) {
          previewImage.src = e.target.result;
          previewContainer.style.display = 'block';
        };
        reader.readAsDataURL(file);
      } else {
        previewContainer.style.display = 'none';
      }
    });
  }

  // 上傳表單提交
  if (avatarForm) {
    avatarForm.addEventListener('submit', function(e) {
      e.preventDefault();
      
      const formData = new FormData();
      const file = avatarInput.files[0];
      
      if (!file) {
        alert('請選擇要上傳的圖片');
        return;
      }
      
      formData.append('avatar', file);
      
      // 顯示進度條，隱藏按鈕
      uploadProgress.style.display = 'block';
      uploadBtn.disabled = true;
      
      // 發送請求 (假設用戶ID為1，實際應該從會話獲取)
      fetch('/api/users/1/avatar', {
        method: 'POST',
        body: formData
      })
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          alert('頭像上傳成功！');
          // 更新當前頭像顯示
          currentAvatar.src = data.data.avatar_url + '?t=' + Date.now(); // 添加時間戳避免緩存
          // 清空表單
          avatarForm.reset();
          previewContainer.style.display = 'none';
        } else {
          alert('上傳失敗：' + data.message);
        }
      })
      .catch(error => {
        console.error('Error:', error);
        alert('上傳失敗，請重試');
      })
      .finally(() => {
        // 隱藏進度條，恢復按鈕
        uploadProgress.style.display = 'none';
        uploadBtn.disabled = false;
      });
    });
  }

  // 刪除頭像功能
  if (deleteBtn) {
    deleteBtn.addEventListener('click', function() {
      if (!confirm('確定要刪除頭像嗎？')) return;
      
      fetch('/api/users/1/avatar', {
        method: 'DELETE'
      })
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          alert('頭像刪除成功！');
          // 恢復預設頭像
          currentAvatar.src = '/static/images/default_avatar.png';
        } else {
          alert('刪除失敗：' + data.message);
        }
      })
      .catch(error => {
        console.error('Error:', error);
        alert('刪除失敗，請重試');
      });
    });
  }
});