// Network Interceptor - FORÇA BRUTA para bloquear TODAS as conexões localhost em produção
import { shouldUseDemoMode } from '../config/environment.js';
import { mockSinistros, mockDashboardData, simulateApiDelay } from '../services/mockData.js';

// Override global fetch se estivermos em modo demo
if (shouldUseDemoMode()) {
  console.log('🚨 NETWORK INTERCEPTOR ACTIVATED - Blocking all network requests in production');
  
  const originalFetch = window.fetch;
  
  window.fetch = async function(url, options) {
    console.log('🚫 BLOCKED FETCH:', url);
    
    // Analyze URL to return appropriate mock data
    await simulateApiDelay();
    
    let mockResponse;
    
    if (url.includes('/sinistros')) {
      mockResponse = {
        sinistros: mockSinistros,
        total: mockSinistros.length,
        demo_mode: true,
        message: "Demo mode - dados simulados"
      };
    } else if (url.includes('/dashboard')) {
      mockResponse = mockDashboardData;
    } else {
      // Default response for any other endpoint
      mockResponse = {
        demo_mode: true,
        message: "Demo mode - operação simulada",
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
  const originalXHR = window.XMLHttpRequest;
  
  window.XMLHttpRequest = function() {
    console.log('🚫 BLOCKED XMLHttpRequest - Demo Mode Active');
    
    const mockXHR = {
      open: function(method, url) {
        this._url = url;
        this._method = method;
      },
      send: function() {
        setTimeout(() => {
          this.readyState = 4;
          this.status = 200;
          
          // Provide contextual mock data based on URL
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
              message: "Demo mode - operação simulada"
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
  
  // Block WebSocket connections too
  const originalWebSocket = window.WebSocket;
  window.WebSocket = function(url) {
    console.log('🚫 BLOCKED WebSocket:', url);
    throw new Error('WebSocket connections are disabled in demo mode');
  };
  
  // Block EventSource (SSE) connections
  const originalEventSource = window.EventSource;
  window.EventSource = function(url) {
    console.log('🚫 BLOCKED EventSource:', url);
    throw new Error('EventSource connections are disabled in demo mode');
  };
  
  console.log('✅ Complete Network interceptor configured - All network requests blocked');
  console.log('📡 All requests will return contextual mock data');
}

export default {};