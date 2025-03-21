import axios from 'axios';
import { formatApiError } from '../utils/apiUtils';

// API URL - using proxy to handle CORS
const API_URL = '/api/blog';

// Create a new blog
export const createBlog = async (blogData) => {
  try {
    const response = await axios.post(`${API_URL}/create`, blogData);
    return response.data;
  } catch (error) {
    console.error('Error creating blog:', error);
    throw new Error(formatApiError(error));
  }
};

// Get blog generation status
export const getBlogStatus = async (projectId) => {
  try {
    const response = await axios.get(`${API_URL}/${projectId}/status`);
    return response.data;
  } catch (error) {
    console.error('Error fetching blog status:', error);
    throw new Error(formatApiError(error));
  }
};

// Cancel blog generation
export const cancelBlogGeneration = async (projectId) => {
  try {
    const response = await axios.post(`${API_URL}/${projectId}/cancel`);
    return response.data;
  } catch (error) {
    console.error('Error canceling blog generation:', error);
    throw new Error(formatApiError(error));
  }
};

// Get all blogs (To be implemented based on your API)
export const getAllBlogs = async () => {
  try {
    // This endpoint might not exist yet - replace with actual endpoint
    const response = await axios.get('/api/projects?status=COMPLETED');
    return response.data;
  } catch (error) {
    console.error('Error fetching blogs:', error);
    throw new Error(formatApiError(error));
  }
};
