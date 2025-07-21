// Network Interceptor - Demo Mode Only
import { shouldUseDemoMode } from '../config/environment.js';
import { mockSinistros, mockDashboardData, simulateApiDelay } from '../services/mockData.js';

// Only intercept in demo mode
if (shouldUseDemoMode()) {
  console.log('🎭 DEMO MODE NETWORK INTERCEPTOR ACTIVATED');
  
  const originalFetch = window.fetch;
  
  window.fetch = async function(url, options) {
    console.log('🚫 DEMO MODE - INTERCEPTING FETCH:', url);
    
    await simulateApiDelay();
    
    let mockResponse;
    
    if (typeof url === 'string' && url.includes('/sinistros')) {
      mockResponse = {
        sinistros: mockSinistros,
        total: mockSinistros.length,
        demo_mode: true,
        message: "Demo mode ativo - dados simulados"
      };
    } else if (typeof url === 'string' && url.includes('/dashboard')) {
      mockResponse = mockDashboardData;
    } else {
      mockResponse = {
        demo_mode: true,
        message: "Demo mode ativo - operação simulada",
        data: null
      };
    }
    
    return new Response(JSON.stringify(mockResponse), {
      status: 200,
      statusText: 'OK',
      headers: {
        'Content-Type': 'application/json',
      }
    });
  };
  
  // Also override XMLHttpRequest for axios
  window.XMLHttpRequest = function() {
    console.log('🚫 DEMO MODE - INTERCEPTING XMLHttpRequest');
    
    const mockXHR = {
      open: function(method, url) {
        this._url = url;
        this._method = method;
      },
      send: function() {
        setTimeout(() => {
          this.readyState = 4;
          this.status = 200;
          
          let responseData;
          if (this._url && this._url.includes('/sinistros')) {
            responseData = {
              sinistros: mockSinistros,
              total: mockSinistros.length,
              demo_mode: true
            };
          } else {
            responseData = {
              demo_mode: true,
              message: "Demo mode ativo"
            };
          }
          
          this.responseText = JSON.stringify(responseData);
          this.response = this.responseText;
          
          if (this.onreadystatechange) this.onreadystatechange();
          if (this.onload) this.onload();
        }, 500);
      },
      setRequestHeader: () => {},
      addEventListener: function(event, handler) {
        if (event === 'load') this.onload = handler;
        if (event === 'error') this.onerror = handler;
      },
      readyState: 0,
      status: 0,
      responseText: '',
      response: '',
      onreadystatechange: null,
      onload: null,
      onerror: null,
      _url: null,
      _method: null
    };
    
    return mockXHR;
  };
  
  console.log('✅ Demo Mode Network Interceptor Configured');
}

export default {};