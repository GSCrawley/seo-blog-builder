import React from 'react';
import { Box, Button, Typography, Alert } from '@mui/material';
import { Refresh as RefreshIcon } from '@mui/icons-material';

function ErrorState({ message = 'An error occurred.', onRetry }) {
  return (
    <Box
      display="flex"
      flexDirection="column"
      alignItems="center"
      justifyContent="center"
      minHeight="200px"
    >
      <Alert severity="error" sx={{ mb: 2, width: '100%' }}>
        {message}
      </Alert>
      {onRetry && (
        <Button 
          variant="contained" 
          startIcon={<RefreshIcon />} 
          onClick={onRetry}
        >
          Retry
        </Button>
      )}
    </Box>
  );
}

export default ErrorState;
