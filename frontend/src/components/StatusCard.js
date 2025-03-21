import React from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Card,
  CardContent,
  CardActions,
  Typography,
  Button,
  Box,
  Chip,
  LinearProgress,
} from '@mui/material';

function StatusCard({ project }) {
  const navigate = useNavigate();

  const getStatusColor = (status) => {
    switch (status) {
      case 'COMPLETED':
        return 'success';
      case 'IN_PROGRESS':
        return 'primary';
      case 'FAILED':
        return 'error';
      case 'PAUSED':
      case 'CANCELLED':
        return 'warning';
      default:
        return 'default';
    }
  };

  return (
    <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      <CardContent sx={{ flexGrow: 1 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
          <Typography variant="h6" component="div">
            {project.name || `Blog #${project.id.slice(-8)}`}
          </Typography>
          <Chip 
            label={project.status} 
            color={getStatusColor(project.status)} 
            size="small" 
          />
        </Box>
        <Typography color="text.secondary" gutterBottom>
          {project.topic || 'No topic specified'}
        </Typography>
        <Typography variant="body2" color="text.secondary">
          Created: {new Date(project.created_at).toLocaleDateString()}
        </Typography>
        {project.current_stage && (
          <Typography variant="body2" sx={{ mt: 1 }}>
            Current Stage: {project.current_stage.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ')}
          </Typography>
        )}
        {project.status === 'IN_PROGRESS' && (
          <Box sx={{ width: '100%', mt: 2 }}>
            <LinearProgress variant="determinate" value={project.progress || 0} />
            <Typography variant="caption" sx={{ display: 'block', textAlign: 'right', mt: 0.5 }}>
              {project.progress || 0}%
            </Typography>
          </Box>
        )}
      </CardContent>
      <CardActions>
        <Button 
          size="small" 
          onClick={() => navigate(`/blog-status/${project.id}`)}
        >
          View Details
        </Button>
        {project.status === 'COMPLETED' && project.deployment_url && (
          <Button 
            size="small"
            color="primary"
            href={project.deployment_url}
            target="_blank"
            rel="noopener noreferrer"
          >
            View Blog
          </Button>
        )}
      </CardActions>
    </Card>
  );
}

export default StatusCard;
