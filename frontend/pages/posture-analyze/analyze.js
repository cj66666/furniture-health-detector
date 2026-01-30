// pages/posture-analyze/analyze.js
Page({
  data: {
    hasResult: false,
    imagePath: ''
  },

  onLoad(options) {
    // 页面加载
  },

  /**
   * 拍照分析
   */
  takePhoto() {
    const that = this;
    wx.chooseMedia({
      count: 1,
      mediaType: ['image'],
      sourceType: ['camera'],
      success(res) {
        const tempFilePath = res.tempFiles[0].tempFilePath;
        that.setData({
          imagePath: tempFilePath
        });
        that.analyzePosture(tempFilePath);
      },
      fail(err) {
        console.error('拍照失败:', err);
        wx.showToast({
          title: '拍照失败',
          icon: 'none'
        });
      }
    });
  },

  /**
   * 从相册选择
   */
  chooseImage() {
    const that = this;
    wx.chooseMedia({
      count: 1,
      mediaType: ['image'],
      sourceType: ['album'],
      success(res) {
        const tempFilePath = res.tempFiles[0].tempFilePath;
        that.setData({
          imagePath: tempFilePath
        });
        that.analyzePosture(tempFilePath);
      },
      fail(err) {
        console.error('选择图片失败:', err);
        wx.showToast({
          title: '选择图片失败',
          icon: 'none'
        });
      }
    });
  },

  /**
   * 分析坐姿（待实现AI接口）
   */
  analyzePosture(imagePath) {
    wx.showLoading({
      title: '分析中...'
    });

    // TODO: 调用AI分析接口
    setTimeout(() => {
      wx.hideLoading();
      this.setData({
        hasResult: true
      });
      wx.showToast({
        title: '分析完成',
        icon: 'success'
      });
    }, 2000);
  }
});