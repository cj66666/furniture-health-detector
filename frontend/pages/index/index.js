// pages/index/index.js
Page({
  /**
   * 页面的初始数据
   */
  data: {
    // 页面数据
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad(options) {
    // 页面加载时的逻辑
  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow() {
    // 页面显示时的逻辑
  },

  /**
   * 跳转到家具检测页面
   */
  goToFurnitureDetect() {
    wx.navigateTo({
      url: '/pages/furniture-detect/detect',
      fail: (err) => {
        console.error('跳转失败:', err);
        wx.showToast({
          title: '页面跳转失败',
          icon: 'none'
        });
      }
    });
  },

  /**
   * 跳转到坐姿分析页面
   */
  goToPostureAnalyze() {
    wx.navigateTo({
      url: '/pages/posture-analyze/analyze',
      fail: (err) => {
        console.error('跳转失败:', err);
        wx.showToast({
          title: '页面跳转失败',
          icon: 'none'
        });
      }
    });
  },

  /**
   * 显示使用说明
   */
  showUserGuide() {
    wx.showModal({
      title: '使用说明',
      content: '1. 家具识别：拍摄桌椅照片，AI将自动识别并分析摆放的合理性\n\n2. 坐姿分析：通过拍摄坐姿照片，获取专业的健康建议\n\n3. 请在光线充足的环境下拍摄，确保照片清晰\n\n4. 建议定期检测坐姿，养成良好习惯',
      confirmText: '我知道了',
      showCancel: false
    });
  },

  /**
   * 显示免责声明
   */
  showDisclaimer() {
    wx.showModal({
      title: '免责声明',
      content: '本小程序提供的坐姿分析和建议仅供参考，不构成专业医疗意见。\n\n如有身体不适或健康问题，请及时咨询专业医疗机构。\n\n使用本小程序即表示您已阅读并同意此声明。',
      confirmText: '已阅读',
      showCancel: false
    });
  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage() {
    return {
      title: '家具安全健康小助手 - 让健康从正确坐姿开始',
      path: '/pages/index/index',
      imageUrl: '/images/share-poster.png'
    };
  }
});