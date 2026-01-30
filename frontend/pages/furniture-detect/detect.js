// pages/furniture-detect/detect.js
const { detectFurniture, handleError } = require('../../utils/api');

Page({
  data: {
    hasResult: false,
    imagePath: '',
    detectionResult: null,
    isAnalyzing: false
  },

  /**
   * 拍照识别
   */
  takePhoto() {
    this.pickImage(['camera']);
  },

  /**
   * 从相册选择
   */
  chooseImage() {
    this.pickImage(['album']);
  },

  pickImage(sourceType) {
    if (this.data.isAnalyzing) {
      return;
    }

    const onSuccess = (res) => {
      const tempFilePath =
        (res.tempFiles && res.tempFiles[0] && res.tempFiles[0].tempFilePath) ||
        (res.tempFilePaths && res.tempFilePaths[0]);

      if (!tempFilePath) {
        wx.showToast({
          title: '未获取到图片',
          icon: 'none'
        });
        return;
      }

      this.setData({
        imagePath: tempFilePath
      });
      this.analyzeImage(tempFilePath);
    };

    const onFail = (err) => {
      console.error('选择图片失败:', err);
      wx.showToast({
        title: '选择图片失败',
        icon: 'none'
      });
    };

    if (wx.chooseMedia) {
      wx.chooseMedia({
        count: 1,
        mediaType: ['image'],
        sourceType,
        success: onSuccess,
        fail: onFail
      });
      return;
    }

    wx.chooseImage({
      count: 1,
      sizeType: ['compressed', 'original'],
      sourceType,
      success: onSuccess,
      fail: onFail
    });
  },

  /**
   * 分析图片 - 调用后端 API
   */
  analyzeImage(imagePath) {
    if (this.data.isAnalyzing) {
      return;
    }

    this.setData({
      isAnalyzing: true,
      hasResult: false,
      detectionResult: null
    });

    wx.showLoading({
      title: '识别中...',
      mask: true
    });

    detectFurniture(imagePath, true)
      .then((result) => {
        wx.hideLoading();

        console.log('检测结果:', result);

        if (!result || result.success === false || !result.data) {
          const errorMsg = (result && result.error) || '识别失败，请重试';
          this.setData({
            isAnalyzing: false
          });
          wx.showModal({
            title: '识别失败',
            content: errorMsg,
            showCancel: false,
            confirmText: '知道了'
          });
          return;
        }

        this.setData({
          hasResult: true,
          detectionResult: result.data,
          isAnalyzing: false
        });

        wx.showToast({
          title: '识别完成',
          icon: 'success',
          duration: 1500
        });
      })
      .catch((err) => {
        wx.hideLoading();

        const errorMsg = handleError(err);
        console.error('检测失败:', err);

        this.setData({
          isAnalyzing: false
        });

        wx.showModal({
          title: '识别失败',
          content: errorMsg,
          showCancel: false,
          confirmText: '知道了'
        });
      });
  },

  /**
   * 查看详细报告
   */
  viewReport() {
    if (!this.data.detectionResult) {
      return;
    }

    const result = this.data.detectionResult;
    const furnitureType = result.furniture_type || '未知';
    let content = `家具类型: ${furnitureType}\n\n`;

    if (Array.isArray(result.materials) && result.materials.length > 0) {
      result.materials.forEach((material, index) => {
        content += `材料${index + 1}: ${material.material_type || '未知'}\n`;
        if (material.confidence !== undefined && material.confidence !== null) {
          content += `置信度: ${material.confidence}%\n`;
        }
        content += '\n';
      });
    } else {
      content += '未返回材料识别结果。';
    }

    if (result.risk_assessment && result.risk_assessment.risk_level) {
      content += `风险等级: ${result.risk_assessment.risk_level}\n`;
    }
    if (result.risk_assessment && Array.isArray(result.risk_assessment.sensitive_groups) && result.risk_assessment.sensitive_groups.length > 0) {
      content += `敏感人群: ${result.risk_assessment.sensitive_groups.join('、')}\n`;
    }
    if (result.risk_assessment && Array.isArray(result.risk_assessment.health_impacts) && result.risk_assessment.health_impacts.length > 0) {
      content += `健康影响: ${result.risk_assessment.health_impacts.join('、')}\n`;
    }
    if (result.risk_assessment && Array.isArray(result.risk_assessment.recommendations) && result.risk_assessment.recommendations.length > 0) {
      content += `建议: ${result.risk_assessment.recommendations.join('、')}\n`;
    }

    wx.showModal({
      title: '检测报告',
      content,
      showCancel: false,
      confirmText: '知道了'
    });
  },

  /**
   * 生成分享卡片
   */
  generateShareCard() {
    if (!this.data.detectionResult) {
      return;
    }

    wx.navigateTo({
      url: `/pages/share-card/share?reportId=${this.data.detectionResult.report_id || ''}`
    });
  },

  /**
   * 重新检测
   */
  resetDetection() {
    this.setData({
      hasResult: false,
      imagePath: '',
      detectionResult: null,
      isAnalyzing: false
    });
  }
});
