// pages/share-card/share.js
const { generateShareCard, handleError } = require('../../utils/api');

Page({
  data: {
    reportId: '',
    reportData: null,
    shareCardUrl: '',
    isGenerating: false,
    selectedTemplate: 'modern' // modern, classic, minimal
  },

  onLoad(options) {
    // 从上一页传递的参数获取报告ID
    if (options.reportId) {
      this.setData({
        reportId: options.reportId
      });
    }

    // 如果有报告数据，直接使用
    if (options.reportData) {
      try {
        const reportData = JSON.parse(decodeURIComponent(options.reportData));
        this.setData({
          reportData: reportData
        });
        // 自动生成分享卡片
        this.generateCard();
      } catch (e) {
        console.error('解析报告数据失败:', e);
      }
    }
  },

  /**
   * 选择模板
   */
  selectTemplate(e) {
    const template = e.currentTarget.dataset.template;
    this.setData({
      selectedTemplate: template
    });
  },

  /**
   * 生成分享卡片
   */
  generateCard() {
    if (!this.data.reportData && !this.data.reportId) {
      wx.showToast({
        title: '缺少报告数据',
        icon: 'none'
      });
      return;
    }

    if (this.data.isGenerating) {
      return;
    }

    this.setData({
      isGenerating: true
    });

    wx.showLoading({
      title: '生成中...',
      mask: true
    });

    // 准备请求数据
    const requestData = {
      report_id: this.data.reportId,
      template: this.data.selectedTemplate
    };

    // 如果有完整的报告数据，也传递过去
    if (this.data.reportData) {
      requestData.furniture_type = this.data.reportData.furniture_type;
      requestData.materials = this.data.reportData.materials;
    }

    // 调用后端 API 生成分享卡片
    generateShareCard(requestData)
      .then(result => {
        wx.hideLoading();

        console.log('分享卡片生成成功:', result);

        this.setData({
          shareCardUrl: result.card_url,
          isGenerating: false
        });

        wx.showToast({
          title: '生成成功',
          icon: 'success'
        });
      })
      .catch(err => {
        wx.hideLoading();

        const errorMsg = handleError(err);
        console.error('生成分享卡片失败:', err);

        this.setData({
          isGenerating: false
        });

        wx.showModal({
          title: '生成失败',
          content: errorMsg,
          showCancel: false,
          confirmText: '知道了'
        });
      });
  },

  /**
   * 保存卡片到相册
   */
  saveCard() {
    if (!this.data.shareCardUrl) {
      wx.showToast({
        title: '请先生成卡片',
        icon: 'none'
      });
      return;
    }

    wx.showLoading({
      title: '保存中...'
    });

    // 下载图片
    wx.downloadFile({
      url: this.data.shareCardUrl,
      success: (res) => {
        if (res.statusCode === 200) {
          // 保存到相册
          wx.saveImageToPhotosAlbum({
            filePath: res.tempFilePath,
            success: () => {
              wx.hideLoading();
              wx.showToast({
                title: '保存成功',
                icon: 'success'
              });
            },
            fail: (err) => {
              wx.hideLoading();
              if (err.errMsg.includes('auth deny')) {
                wx.showModal({
                  title: '需要授权',
                  content: '请允许访问相册以保存图片',
                  success: (modalRes) => {
                    if (modalRes.confirm) {
                      wx.openSetting();
                    }
                  }
                });
              } else {
                wx.showToast({
                  title: '保存失败',
                  icon: 'none'
                });
              }
            }
          });
        } else {
          wx.hideLoading();
          wx.showToast({
            title: '下载失败',
            icon: 'none'
          });
        }
      },
      fail: () => {
        wx.hideLoading();
        wx.showToast({
          title: '下载失败',
          icon: 'none'
        });
      }
    });
  },

  /**
   * 分享卡片给好友
   */
  shareCard() {
    if (!this.data.shareCardUrl) {
      wx.showToast({
        title: '请先生成卡片',
        icon: 'none'
      });
      return;
    }

    wx.showShareMenu({
      withShareTicket: true,
      menus: ['shareAppMessage', 'shareTimeline']
    });

    wx.showToast({
      title: '请点击右上角分享',
      icon: 'none'
    });
  },

  /**
   * 分享到微信
   */
  onShareAppMessage() {
    return {
      title: '我的家具健康检测报告',
      path: '/pages/share-card/share?reportId=' + this.data.reportId,
      imageUrl: this.data.shareCardUrl || '/images/share-card.png'
    };
  },

  /**
   * 分享到朋友圈
   */
  onShareTimeline() {
    return {
      title: '家具安全健康小助手 - 我的健康报告',
      imageUrl: this.data.shareCardUrl
    };
  },

  /**
   * 重新生成
   */
  regenerateCard() {
    this.generateCard();
  }
});