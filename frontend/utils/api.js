/**
 * API utils - wraps backend requests
 */

const CONFIG = {
  // Dev uses local backend
  BASE_URL: 'http://localhost:8001/api/v1',
  TIMEOUT: 30000,
  MAX_IMAGE_SIZE: 10
};

const request = (options) =>
  new Promise((resolve, reject) => {
    wx.request({
      ...options,
      timeout: CONFIG.TIMEOUT,
      success: (res) => {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          resolve(res.data);
          return;
        }
        reject({
          code: res.statusCode,
          message: (res.data && res.data.detail) || '请求失败',
          data: res.data
        });
      },
      fail: (err) => {
        reject({
          code: -1,
          message: '网络请求失败',
          error: err
        });
      }
    });
  });

/**
 * 家具检测 API
 * @param {string} imagePath - 本地图片路径
 * @param {boolean} disclaimerAccepted - 是否接受免责声明
 */
const detectFurniture = (imagePath, disclaimerAccepted = true) =>
  new Promise((resolve, reject) => {
    wx.getFileInfo({
      filePath: imagePath,
      success: (fileInfo) => {
        const sizeMB = fileInfo.size / (1024 * 1024);
        if (sizeMB > CONFIG.MAX_IMAGE_SIZE) {
          reject({
            code: -2,
            message: `图片大小超过限制（${CONFIG.MAX_IMAGE_SIZE}MB）`
          });
          return;
        }

        wx.uploadFile({
          url: `${CONFIG.BASE_URL}/furniture/detect`,
          filePath: imagePath,
          name: 'image',
          formData: {
            disclaimer_accepted: disclaimerAccepted ? 'true' : 'false'
          },
          timeout: CONFIG.TIMEOUT,
          success: (res) => {
            let data;
            try {
              data = typeof res.data === 'string' ? JSON.parse(res.data) : res.data;
            } catch (e) {
              reject({
                code: -3,
                message: '响应数据解析失败',
                error: e
              });
              return;
            }

            if (res.statusCode >= 200 && res.statusCode < 300) {
              resolve(data);
              return;
            }

            reject({
              code: res.statusCode,
              message: (data && data.detail) || '检测失败',
              data
            });
          },
          fail: (err) => {
            reject({
              code: -1,
              message: '图片上传失败',
              error: err
            });
          }
        });
      },
      fail: (err) => {
        reject({
          code: -4,
          message: '获取图片信息失败',
          error: err
        });
      }
    });
  });

const generateShareCard = (reportData) =>
  request({
    url: `${CONFIG.BASE_URL}/share/generate`,
    method: 'POST',
    data: reportData,
    header: {
      'content-type': 'application/json'
    }
  });

const healthCheck = () =>
  request({
    url: `${CONFIG.BASE_URL}/health`,
    method: 'GET'
  });

const handleError = (error) => {
  console.error('API Error:', error);

  const errorMessages = {
    400: '请求参数错误',
    401: '未授权访问',
    403: '禁止访问',
    404: '接口不存在',
    500: '服务器错误',
    502: '网关错误',
    503: '服务暂时不可用',
    '-1': '网络连接失败，请检查网络',
    '-2': '图片大小超过限制',
    '-3': '数据解析失败',
    '-4': '获取图片信息失败'
  };

  return (error && error.message) || errorMessages[error.code] || '未知错误';
};

module.exports = {
  CONFIG,
  detectFurniture,
  generateShareCard,
  healthCheck,
  handleError
};
