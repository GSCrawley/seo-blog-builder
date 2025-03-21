import React, { useState } from 'react';
import {
  Typography,
  Box,
  Paper,
  Grid,
  TextField,
  Button,
  Divider,
  Switch,
  FormControlLabel,
  FormGroup,
  Snackbar,
  Alert,
  Card,
  CardContent,
  CardHeader,
  Tab,
  Tabs,
} from '@mui/material';
import {
  Save as SaveIcon,
  Key as ApiKeyIcon,
  Sync as SyncIcon,
  Email as EmailIcon,
  BrandingWatermark as BrandingIcon,
  Storage as StorageIcon,
} from '@mui/icons-material';

// Tab Panel component
function TabPanel({ children, value, index, ...other }) {
  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`settings-tabpanel-${index}`}
      aria-labelledby={`settings-tab-${index}`}
      {...other}
    >
      {value === index && (
        <Box sx={{ p: 3 }}>
          {children}
        </Box>
      )}
    </div>
  );
}

function Settings() {
  const [activeTab, setActiveTab] = useState(0);
  const [settings, setSettings] = useState({
    apiKeys: {
      anthropic: '',
      openai: '',
      googleAds: '',
    },
    email: {
      smtpServer: '',
      username: '',
      password: '',
      fromEmail: '',
      emailEnabled: false,
    },
    branding: {
      defaultDomain: 'seoblog.ai',
      useDefaultBranding: true,
      defaultLogo: '',
      defaultColor: '#1976d2',
    },
  });
  const [snackbar, setSnackbar] = useState({
    open: false,
    message: '',
    severity: 'success',
  });

  const handleTabChange = (event, newValue) => {
    setActiveTab(newValue);
  };

  const handleSettingChange = (section, field) => (event) => {
    const value = event.target.type === 'checkbox' ? event.target.checked : event.target.value;
    setSettings({
      ...settings,
      [section]: {
        ...settings[section],
        [field]: value,
      },
    });
  };

  const handleSaveSettings = () => {
    // In a real app, this would save to an API endpoint
    console.log('Saving settings:', settings);
    
    // Show success message
    setSnackbar({
      open: true,
      message: 'Settings saved successfully',
      severity: 'success',
    });
  };

  const handleCloseSnackbar = () => {
    setSnackbar({ ...snackbar, open: false });
  };

  return (
    <Box>
      <Typography variant="h4" component="h1" gutterBottom>
        Settings
      </Typography>
      <Typography variant="body1" color="text.secondary" sx={{ mb: 3 }}>
        Configure your SEO Blog Builder application settings.
      </Typography>

      <Paper sx={{ mb: 3 }}>
        <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
          <Tabs value={activeTab} onChange={handleTabChange} aria-label="settings tabs">
            <Tab icon={<ApiKeyIcon />} iconPosition="start" label="API Keys" />
            <Tab icon={<EmailIcon />} iconPosition="start" label="Email" />
            <Tab icon={<BrandingIcon />} iconPosition="start" label="Branding" />
            <Tab icon={<StorageIcon />} iconPosition="start" label="Storage" />
          </Tabs>
        </Box>

        {/* API Keys Tab */}
        <TabPanel value={activeTab} index={0}>
          <Grid container spacing={3}>
            <Grid item xs={12}>
              <Typography variant="h6" gutterBottom>
                API Keys
              </Typography>
              <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
                Configure API keys for various services used by the application.
              </Typography>
            </Grid>

            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="Anthropic API Key"
                value={settings.apiKeys.anthropic}
                onChange={handleSettingChange('apiKeys', 'anthropic')}
                type="password"
                variant="outlined"
                margin="normal"
                helperText="Used for Claude AI services"
              />
            </Grid>

            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="OpenAI API Key"
                value={settings.apiKeys.openai}
                onChange={handleSettingChange('apiKeys', 'openai')}
                type="password"
                variant="outlined"
                margin="normal"
                helperText="Used for GPT services"
              />
            </Grid>

            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="Google Ads API Key"
                value={settings.apiKeys.googleAds}
                onChange={handleSettingChange('apiKeys', 'googleAds')}
                type="password"
                variant="outlined"
                margin="normal"
                helperText="Used for keyword research (optional)"
              />
            </Grid>
          </Grid>
        </TabPanel>

        {/* Email Tab */}
        <TabPanel value={activeTab} index={1}>
          <Grid container spacing={3}>
            <Grid item xs={12}>
              <Typography variant="h6" gutterBottom>
                Email Settings
              </Typography>
              <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
                Configure email settings for notifications and reports.
              </Typography>
            </Grid>

            <Grid item xs={12}>
              <FormGroup>
                <FormControlLabel
                  control={
                    <Switch
                      checked={settings.email.emailEnabled}
                      onChange={handleSettingChange('email', 'emailEnabled')}
                    />
                  }
                  label="Enable Email Notifications"
                />
              </FormGroup>
            </Grid>

            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="SMTP Server"
                value={settings.email.smtpServer}
                onChange={handleSettingChange('email', 'smtpServer')}
                variant="outlined"
                margin="normal"
                disabled={!settings.email.emailEnabled}
              />
            </Grid>

            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="SMTP Username"
                value={settings.email.username}
                onChange={handleSettingChange('email', 'username')}
                variant="outlined"
                margin="normal"
                disabled={!settings.email.emailEnabled}
              />
            </Grid>

            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="SMTP Password"
                value={settings.email.password}
                onChange={handleSettingChange('email', 'password')}
                type="password"
                variant="outlined"
                margin="normal"
                disabled={!settings.email.emailEnabled}
              />
            </Grid>

            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="From Email Address"
                value={settings.email.fromEmail}
                onChange={handleSettingChange('email', 'fromEmail')}
                variant="outlined"
                margin="normal"
                disabled={!settings.email.emailEnabled}
              />
            </Grid>

            <Grid item xs={12}>
              <Button
                variant="outlined"
                startIcon={<SyncIcon />}
                disabled={!settings.email.emailEnabled}
              >
                Test Email Configuration
              </Button>
            </Grid>
          </Grid>
        </TabPanel>

        {/* Branding Tab */}
        <TabPanel value={activeTab} index={2}>
          <Grid container spacing={3}>
            <Grid item xs={12}>
              <Typography variant="h6" gutterBottom>
                Branding & Appearance
              </Typography>
              <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
                Configure default branding settings for generated blogs.
              </Typography>
            </Grid>

            <Grid item xs={12}>
              <FormGroup>
                <FormControlLabel
                  control={
                    <Switch
                      checked={settings.branding.useDefaultBranding}
                      onChange={handleSettingChange('branding', 'useDefaultBranding')}
                    />
                  }
                  label="Use Default Branding for New Blogs"
                />
              </FormGroup>
            </Grid>

            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="Default Domain"
                value={settings.branding.defaultDomain}
                onChange={handleSettingChange('branding', 'defaultDomain')}
                variant="outlined"
                margin="normal"
                helperText="Base domain for all blogs (e.g., seoblog.ai)"
              />
            </Grid>

            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="Default Brand Color"
                value={settings.branding.defaultColor}
                onChange={handleSettingChange('branding', 'defaultColor')}
                variant="outlined"
                margin="normal"
                type="color"
                helperText="Primary color for new blogs"
              />
            </Grid>
          </Grid>
        </TabPanel>

        {/* Storage Tab */}
        <TabPanel value={activeTab} index={3}>
          <Grid container spacing={3}>
            <Grid item xs={12}>
              <Typography variant="h6" gutterBottom>
                Storage Settings
              </Typography>
              <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
                Configure storage settings for blog content and assets.
              </Typography>
            </Grid>

            <Grid item xs={12} md={6}>
              <Card>
                <CardHeader title="Storage Statistics" />
                <CardContent>
                  <Grid container spacing={2}>
                    <Grid item xs={6}>
                      <Typography variant="subtitle2" color="text.secondary">Total Blogs:</Typography>
                      <Typography variant="h6">15</Typography>
                    </Grid>
                    <Grid item xs={6}>
                      <Typography variant="subtitle2" color="text.secondary">Total Articles:</Typography>
                      <Typography variant="h6">87</Typography>
                    </Grid>
                    <Grid item xs={6}>
                      <Typography variant="subtitle2" color="text.secondary">Storage Used:</Typography>
                      <Typography variant="h6">256 MB</Typography>
                    </Grid>
                    <Grid item xs={6}>
                      <Typography variant="subtitle2" color="text.secondary">Storage Limit:</Typography>
                      <Typography variant="h6">5 GB</Typography>
                    </Grid>
                  </Grid>
                </CardContent>
              </Card>
            </Grid>

            <Grid item xs={12} md={6}>
              <Card>
                <CardHeader title="Backup & Restore" />
                <CardContent>
                  <Box sx={{ mb: 2 }}>
                    <Button variant="outlined" fullWidth sx={{ mb: 1 }}>
                      Backup All Data
                    </Button>
                    <Typography variant="caption" color="text.secondary">
                      Last backup: Never
                    </Typography>
                  </Box>
                  <Box>
                    <Button variant="outlined" fullWidth color="warning">
                      Restore From Backup
                    </Button>
                  </Box>
                </CardContent>
              </Card>
            </Grid>
          </Grid>
        </TabPanel>

        <Box sx={{ p: 3, borderTop: 1, borderColor: 'divider', display: 'flex', justifyContent: 'flex-end' }}>
          <Button 
            variant="contained" 
            color="primary" 
            startIcon={<SaveIcon />}
            onClick={handleSaveSettings}
          >
            Save Settings
          </Button>
        </Box>
      </Paper>

      <Snackbar
        open={snackbar.open}
        autoHideDuration={6000}
        onClose={handleCloseSnackbar}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
      >
        <Alert onClose={handleCloseSnackbar} severity={snackbar.severity} sx={{ width: '100%' }}>
          {snackbar.message}
        </Alert>
      </Snackbar>
    </Box>
  );
}

export default Settings;
