import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Typography,
  Box,
  Paper,
  Grid,
  Card,
  CardContent,
  CardActions,
  Button,
  Chip,
  LinearProgress,
  Divider,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Alert,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogContentText,
  DialogActions,
  Link,
} from '@mui/material';
import LoadingState from '../components/LoadingState';
import ErrorState from '../components/ErrorState';
import {
  CheckCircle as CheckCircleIcon,
  Cancel as CancelIcon,
  Pending as PendingIcon,
  Error as ErrorIcon,
  OpenInNew as OpenInNewIcon,
  Refresh as RefreshIcon,
  AssignmentTurnedIn as TaskIcon,
} from '@mui/icons-material';
import { getBlogStatus, cancelBlogGeneration } from '../services/blogService';

function BlogStatus() {
  const { projectId } = useParams();
  const navigate = useNavigate();
  const [status, setStatus] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [refreshInterval, setRefreshInterval] = useState(null);
  const [cancelDialogOpen, setCancelDialogOpen] = useState(false);
  
  const fetchStatus = async () => {
    try {
      const data = await getBlogStatus(projectId);
      setStatus(data);
      setLoading(false);
      
      // If the blog generation is complete or failed, stop refreshing
      if (data.status === 'COMPLETED' || data.status === 'FAILED') {
        clearInterval(refreshInterval);
        setRefreshInterval(null);
      }
    } catch (err) {
      setError('Failed to load blog status. Please try again.');
      setLoading(false);
      clearInterval(refreshInterval);
      setRefreshInterval(null);
    }
  };
  
  useEffect(() => {
    fetchStatus();
    
    // Set up auto-refresh every 10 seconds if not already set
    if (!refreshInterval) {
      const interval = setInterval(fetchStatus, 10000);
      setRefreshInterval(interval);
    }
    
    // Clean up interval on component unmount
    return () => {
      if (refreshInterval) {
        clearInterval(refreshInterval);
      }
    };
  }, [projectId]);
  
  const handleRefresh = () => {
    setLoading(true);
    fetchStatus();
  };
  
  const handleCancel = async () => {
    try {
      await cancelBlogGeneration(projectId);
      setCancelDialogOpen(false);
      // Fetch updated status
      fetchStatus();
    } catch (err) {
      setError('Failed to cancel blog generation.');
      setCancelDialogOpen(false);
    }
  };
  
  const getStatusIcon = (stageStatus) => {
    switch (stageStatus) {
      case 'completed':
        return <CheckCircleIcon color="success" />;
      case 'in_progress':
        return <PendingIcon color="primary" />;
      case 'failed':
        return <ErrorIcon color="error" />;
      default:
        return <PendingIcon color="disabled" />;
    }
  };
  
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
  
  if (loading && !status) {
    return <LoadingState message="Loading blog status..." />;
  }
  
  if (error) {
    return <ErrorState message={error} onRetry={handleRefresh} />;
  }
  
  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Blog Status
        </Typography>
        <Box>
          <Button 
            variant="outlined" 
            startIcon={<RefreshIcon />} 
            onClick={handleRefresh}
            sx={{ mr: 1 }}
            disabled={loading}
          >
            Refresh
          </Button>
          {status?.status === 'IN_PROGRESS' && (
            <Button 
              variant="outlined" 
              color="error" 
              startIcon={<CancelIcon />} 
              onClick={() => setCancelDialogOpen(true)}
              disabled={loading}
            >
              Cancel
            </Button>
          )}
        </Box>
      </Box>
      
      {status && (
        <>
          <Paper sx={{ p: 3, mb: 3 }}>
            <Grid container spacing={3}>
              <Grid item xs={12} md={8}>
                <Typography variant="h6" gutterBottom>
                  Project Details
                </Typography>
                <Typography variant="body1">
                  <strong>Topic:</strong> {status.topic}
                </Typography>
                <Typography variant="body1">
                  <strong>Current Stage:</strong> {status.current_stage || 'Initializing'}
                </Typography>
                {status.status === 'COMPLETED' && status.deployment_url && (
                  <Box sx={{ mt: 2 }}>
                    <Typography variant="body1">
                      <strong>Blog URL:</strong>{' '}
                      <Link 
                        href={status.deployment_url} 
                        target="_blank" 
                        rel="noopener noreferrer"
                        sx={{ display: 'inline-flex', alignItems: 'center' }}
                      >
                        {status.deployment_url}
                        <OpenInNewIcon sx={{ ml: 0.5, fontSize: '0.875rem' }} />
                      </Link>
                    </Typography>
                  </Box>
                )}
              </Grid>
              <Grid item xs={12} md={4} sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
                <Chip 
                  label={status.status} 
                  color={getStatusColor(status.status)} 
                  sx={{ fontSize: '1.1rem', px: 2, py: 3 }}
                />
                <Typography variant="body2" sx={{ mt: 1, color: 'text.secondary' }}>
                  {status.progress}% Complete
                </Typography>
                <Box sx={{ width: '100%', mt: 1 }}>
                  <LinearProgress variant="determinate" value={status.progress || 0} />
                </Box>
              </Grid>
            </Grid>
          </Paper>
          
          <Grid container spacing={3}>
            <Grid item xs={12} md={6}>
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    Progress Stages
                  </Typography>
                  <List>
                    {status.stages && Object.entries(status.stages).map(([stage, stageInfo]) => (
                      <ListItem key={stage}>
                        <ListItemIcon>
                          {getStatusIcon(stageInfo.status)}
                        </ListItemIcon>
                        <ListItemText 
                          primary={stage.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ')} 
                          secondary={stageInfo.status === 'in_progress' ? 'In Progress' : stageInfo.status.charAt(0).toUpperCase() + stageInfo.status.slice(1)}
                        />
                      </ListItem>
                    ))}
                  </List>
                </CardContent>
              </Card>
            </Grid>
            
            <Grid item xs={12} md={6}>
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    Activity Timeline
                  </Typography>
                  {status.timeline && status.timeline.length > 0 ? (
                    <List>
                      {status.timeline.map((event, index) => (
                        <ListItem key={index} alignItems="flex-start">
                          <ListItemIcon>
                            <TaskIcon color="primary" />
                          </ListItemIcon>
                          <ListItemText
                            primary={event.description}
                            secondary={new Date(event.timestamp).toLocaleString()}
                          />
                        </ListItem>
                      ))}
                    </List>
                  ) : (
                    <Typography variant="body2" color="text.secondary">
                      No activity recorded yet.
                    </Typography>
                  )}
                </CardContent>
                <CardActions>
                  <Button 
                    size="small" 
                    onClick={() => navigate('/blog-generator')}
                  >
                    Create Another Blog
                  </Button>
                  <Button 
                    size="small" 
                    onClick={() => navigate('/')}
                  >
                    Back to Dashboard
                  </Button>
                </CardActions>
              </Card>
            </Grid>
          </Grid>
          
          {/* Error display if something went wrong */}
          {status.status === 'FAILED' && (
            <Alert severity="error" sx={{ mt: 3 }}>
              <Typography variant="body1" gutterBottom>
                <strong>Blog generation failed.</strong>
              </Typography>
              {status.error && (
                <Typography variant="body2">
                  Error details: {status.error}
                </Typography>
              )}
            </Alert>
          )}
          
          {/* Cancel Confirmation Dialog */}
          <Dialog
            open={cancelDialogOpen}
            onClose={() => setCancelDialogOpen(false)}
          >
            <DialogTitle>Cancel Blog Generation</DialogTitle>
            <DialogContent>
              <DialogContentText>
                Are you sure you want to cancel this blog generation process? This action cannot be undone.
              </DialogContentText>
            </DialogContent>
            <DialogActions>
              <Button onClick={() => setCancelDialogOpen(false)}>No, Continue</Button>
              <Button onClick={handleCancel} color="error" autoFocus>
                Yes, Cancel Generation
              </Button>
            </DialogActions>
          </Dialog>
        </>
      )}
    </Box>
  );
}

export default BlogStatus;
