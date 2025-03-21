import React from 'react';
import { Box, Typography, Button, Paper } from '@mui/material';

/**
 * Component to display when there is no data to show
 * 
 * @param {Object} props Component props
 * @param {string} props.title Empty state title
 * @param {string} props.message Empty state description
 * @param {string} props.buttonText Text for the action button
 * @param {Function} props.buttonAction Function to call when button is clicked
 * @param {boolean} props.showButton Whether to show the action button
 * @param {React.ReactNode} props.icon Icon to display
 */
function EmptyState({
  title = 'No data found',
  message = 'There is no data to display at this time.',
  buttonText = 'Get Started',
  buttonAction,
  showButton = true,
  icon,
}) {
  return (
    <Paper
      sx={{
        p: 4,
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        textAlign: 'center',
        minHeight: '200px',
        justifyContent: 'center',
      }}
    >
      {icon && (
        <Box sx={{ mb: 2, color: 'text.secondary' }}>
          {icon}
        </Box>
      )}
      <Typography variant="h6" gutterBottom>
        {title}
      </Typography>
      <Typography variant="body1" color="text.secondary" sx={{ mb: 3 }}>
        {message}
      </Typography>
      {showButton && buttonAction && (
        <Button variant="contained" onClick={buttonAction}>
          {buttonText}
        </Button>
      )}
    </Paper>
  );
}

export default EmptyState;
