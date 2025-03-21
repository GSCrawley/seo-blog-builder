import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Typography,
  Grid,
  Button,
  Box,
  Divider,
} from '@mui/material';
import { Add as AddIcon, Article as ArticleIcon } from '@mui/icons-material';
import { getAllBlogs } from '../services/blogService';
import LoadingState from '../components/LoadingState';
import ErrorState from '../components/ErrorState';
import EmptyState from '../components/EmptyState';
import StatusCard from '../components/StatusCard';

function Dashboard() {
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchProjects = async () => {
      try {
        const data = await getAllBlogs();
        setProjects(data);
        setLoading(false);
      } catch (err) {
        setError('Failed to load projects. Please try again later.');
        setLoading(false);
      }
    };

    fetchProjects();
  }, []);

  const getStatusColor = (status) => {
    switch (status) {
      case 'COMPLETED':
        return 'success';
      case 'IN_PROGRESS':
        return 'primary';
      case 'FAILED':
        return 'error';
      case 'PAUSED':
        return 'warning';
      default:
        return 'default';
    }
  };

  const renderProgress = (project) => {
    if (project.status === 'IN_PROGRESS') {
      return <LinearProgress variant="determinate" value={project.progress || 0} />;
    }
    return null;
  };

  if (loading) {
    return <LoadingState message="Loading your projects..." />;
  }

  if (error) {
    return <ErrorState message={error} onRetry={() => window.location.reload()} />;
  }

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Dashboard
        </Typography>
        <Button 
          variant="contained" 
          color="primary" 
          onClick={() => navigate('/blog-generator')}
          startIcon={<AddIcon />}
        >
          Create New Blog
        </Button>
      </Box>

      <Divider sx={{ mb: 3 }} />

      <Typography variant="h6" gutterBottom>
        Recent Projects
      </Typography>

      {projects.length === 0 ? (
        <EmptyState
          title="No blogs yet"
          message="You don't have any blog projects yet. Get started by creating your first SEO-optimized blog."
          buttonText="Create New Blog"
          buttonAction={() => navigate('/blog-generator')}
          icon={<ArticleIcon sx={{ fontSize: 48 }} />}
        />
      ) : (
        <Grid container spacing={3}>
          {projects.map((project) => (
            <Grid item xs={12} md={6} lg={4} key={project.id}>
              <StatusCard project={project} />
            </Grid>
          ))}
        </Grid>
      )}
    </Box>
  );
}

export default Dashboard;
