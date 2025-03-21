import React, { useState } from 'react';
import {
  Typography,
  Box,
  Paper,
  Grid,
  Card,
  CardContent,
  CardHeader,
  Divider,
  Button,
  MenuItem,
  Select,
  FormControl,
  InputLabel,
  Tabs,
  Tab,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
} from '@mui/material';
import {
  ShowChart as ChartIcon,
  TrendingUp as TrendingUpIcon,
  TrendingDown as TrendingDownIcon,
  Equalizer as EqualizerIcon,
  Person as PersonIcon,
  Language as LanguageIcon,
  Link as LinkIcon,
} from '@mui/icons-material';

// Tab Panel component
function TabPanel({ children, value, index, ...other }) {
  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`analytics-tabpanel-${index}`}
      aria-labelledby={`analytics-tab-${index}`}
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

// Stat Card Component
function StatCard({ title, value, icon, trend, trendValue, trendLabel }) {
  return (
    <Card>
      <CardContent>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
          <Box>
            <Typography variant="subtitle2" color="text.secondary" gutterBottom>
              {title}
            </Typography>
            <Typography variant="h4">
              {value}
            </Typography>
          </Box>
          <Box sx={{ p: 1, bgcolor: 'action.hover', borderRadius: 1 }}>
            {icon}
          </Box>
        </Box>
        {trend && (
          <Box sx={{ display: 'flex', alignItems: 'center', mt: 2 }}>
            {trend === 'up' ? (
              <TrendingUpIcon color="success" fontSize="small" />
            ) : (
              <TrendingDownIcon color="error" fontSize="small" />
            )}
            <Typography 
              variant="body2"
              color={trend === 'up' ? 'success.main' : 'error.main'}
              sx={{ ml: 0.5 }}
            >
              {trendValue} {trendLabel}
            </Typography>
          </Box>
        )}
      </CardContent>
    </Card>
  );
}

function Analytics() {
  const [period, setPeriod] = useState('7days');
  const [activeTab, setActiveTab] = useState(0);

  const handlePeriodChange = (event) => {
    setPeriod(event.target.value);
  };

  const handleTabChange = (event, newValue) => {
    setActiveTab(newValue);
  };

  // Mock data for content performance
  const contentPerformanceData = [
    { 
      title: '10 Essential Tips for SEO Success', 
      views: 1245, 
      uniqueVisitors: 987, 
      avgTimeOnPage: '4:12', 
      bounceRate: '38.2%',
      conversions: 23 
    },
    { 
      title: 'How to Optimize Your Blog for Google', 
      views: 986, 
      uniqueVisitors: 754, 
      avgTimeOnPage: '3:45', 
      bounceRate: '42.5%',
      conversions: 18 
    },
    { 
      title: 'The Ultimate Guide to Affiliate Marketing', 
      views: 1542, 
      uniqueVisitors: 1203, 
      avgTimeOnPage: '5:31', 
      bounceRate: '31.8%',
      conversions: 47 
    },
    { 
      title: 'Best WordPress Plugins for SEO in 2024', 
      views: 856, 
      uniqueVisitors: 682, 
      avgTimeOnPage: '2:58', 
      bounceRate: '45.1%',
      conversions: 15 
    },
    { 
      title: '5 Case Studies of Successful Content Marketing', 
      views: 724, 
      uniqueVisitors: 598, 
      avgTimeOnPage: '3:22', 
      bounceRate: '40.3%',
      conversions: 12 
    },
  ];

  // Mock data for keyword rankings
  const keywordRankingsData = [
    { keyword: 'seo blog builder', position: 3, change: '+2', searchVolume: '1,200' },
    { keyword: 'how to create seo blog', position: 5, change: '-1', searchVolume: '2,400' },
    { keyword: 'affiliate blog generator', position: 1, change: '+4', searchVolume: '890' },
    { keyword: 'blog content optimization', position: 8, change: '+1', searchVolume: '3,600' },
    { keyword: 'automated blog creation', position: 12, change: '-3', searchVolume: '1,800' },
  ];

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Analytics
        </Typography>
        <FormControl variant="outlined" size="small" sx={{ minWidth: 150 }}>
          <InputLabel id="period-select-label">Time Period</InputLabel>
          <Select
            labelId="period-select-label"
            id="period-select"
            value={period}
            onChange={handlePeriodChange}
            label="Time Period"
          >
            <MenuItem value="7days">Last 7 Days</MenuItem>
            <MenuItem value="30days">Last 30 Days</MenuItem>
            <MenuItem value="90days">Last 90 Days</MenuItem>
            <MenuItem value="year">Last Year</MenuItem>
          </Select>
        </FormControl>
      </Box>

      <Typography variant="body1" color="text.secondary" sx={{ mb: 3 }}>
        Track performance of your SEO optimized blogs and content.
      </Typography>

      {/* Overview Cards */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Total Views"
            value="12,584"
            icon={<EqualizerIcon />}
            trend="up"
            trendValue="+12.5%"
            trendLabel="vs previous period"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Unique Visitors"
            value="4,826"
            icon={<PersonIcon />}
            trend="up"
            trendValue="+8.3%"
            trendLabel="vs previous period"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Avg. Time on Page"
            value="3:42"
            icon={<ChartIcon />}
            trend="up"
            trendValue="+0:18"
            trendLabel="vs previous period"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Bounce Rate"
            value="42.1%"
            icon={<LanguageIcon />}
            trend="down"
            trendValue="-3.8%"
            trendLabel="vs previous period"
          />
        </Grid>
      </Grid>

      {/* Main Analytics Content */}
      <Paper sx={{ mb: 4 }}>
        <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
          <Tabs value={activeTab} onChange={handleTabChange} aria-label="analytics tabs">
            <Tab label="Traffic Overview" />
            <Tab label="Content Performance" />
            <Tab label="SEO Metrics" />
            <Tab label="Conversions" />
          </Tabs>
        </Box>

        {/* Traffic Overview Tab */}
        <TabPanel value={activeTab} index={0}>
          <Box sx={{ height: '300px', display: 'flex', alignItems: 'center', justifyContent: 'center', bgcolor: 'action.hover', borderRadius: 1, mb: 3 }}>
            <Typography variant="h6" color="text.secondary">
              Traffic Overview Chart (Placeholder)
            </Typography>
            {/* In a real application, this would be a chart component */}
          </Box>
          
          <Grid container spacing={3}>
            <Grid item xs={12} md={6}>
              <Card>
                <CardHeader title="Traffic Sources" />
                <CardContent>
                  <Box sx={{ height: '200px', display: 'flex', alignItems: 'center', justifyContent: 'center', bgcolor: 'action.hover', borderRadius: 1 }}>
                    <Typography variant="body1" color="text.secondary">
                      Traffic Sources Chart (Placeholder)
                    </Typography>
                  </Box>
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={12} md={6}>
              <Card>
                <CardHeader title="Device Distribution" />
                <CardContent>
                  <Box sx={{ height: '200px', display: 'flex', alignItems: 'center', justifyContent: 'center', bgcolor: 'action.hover', borderRadius: 1 }}>
                    <Typography variant="body1" color="text.secondary">
                      Device Distribution Chart (Placeholder)
                    </Typography>
                  </Box>
                </CardContent>
              </Card>
            </Grid>
          </Grid>
        </TabPanel>

        {/* Content Performance Tab */}
        <TabPanel value={activeTab} index={1}>
          <TableContainer>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Title</TableCell>
                  <TableCell align="right">Views</TableCell>
                  <TableCell align="right">Unique Visitors</TableCell>
                  <TableCell align="right">Avg. Time</TableCell>
                  <TableCell align="right">Bounce Rate</TableCell>
                  <TableCell align="right">Conversions</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {contentPerformanceData.map((row) => (
                  <TableRow
                    key={row.title}
                    sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
                  >
                    <TableCell component="th" scope="row">
                      <Box sx={{ display: 'flex', alignItems: 'center' }}>
                        <LinkIcon fontSize="small" sx={{ mr: 1, color: 'primary.main' }} />
                        {row.title}
                      </Box>
                    </TableCell>
                    <TableCell align="right">{row.views.toLocaleString()}</TableCell>
                    <TableCell align="right">{row.uniqueVisitors.toLocaleString()}</TableCell>
                    <TableCell align="right">{row.avgTimeOnPage}</TableCell>
                    <TableCell align="right">{row.bounceRate}</TableCell>
                    <TableCell align="right">{row.conversions}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </TabPanel>

        {/* SEO Metrics Tab */}
        <TabPanel value={activeTab} index={2}>
          <Grid container spacing={3}>
            <Grid item xs={12} md={6}>
              <Card>
                <CardHeader title="Keyword Rankings" />
                <CardContent>
                  <TableContainer>
                    <Table>
                      <TableHead>
                        <TableRow>
                          <TableCell>Keyword</TableCell>
                          <TableCell align="right">Position</TableCell>
                          <TableCell align="right">Change</TableCell>
                          <TableCell align="right">Search Volume</TableCell>
                        </TableRow>
                      </TableHead>
                      <TableBody>
                        {keywordRankingsData.map((row) => (
                          <TableRow
                            key={row.keyword}
                            sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
                          >
                            <TableCell component="th" scope="row">
                              {row.keyword}
                            </TableCell>
                            <TableCell align="right">{row.position}</TableCell>
                            <TableCell 
                              align="right"
                              sx={{ 
                                color: row.change.startsWith('+') 
                                  ? 'success.main' 
                                  : row.change.startsWith('-') 
                                    ? 'error.main' 
                                    : 'inherit' 
                              }}
                            >
                              {row.change}
                            </TableCell>
                            <TableCell align="right">{row.searchVolume}</TableCell>
                          </TableRow>
                        ))}
                      </TableBody>
                    </Table>
                  </TableContainer>
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={12} md={6}>
              <Card>
                <CardHeader title="SEO Health" />
                <CardContent>
                  <Box sx={{ height: '280px', display: 'flex', alignItems: 'center', justifyContent: 'center', bgcolor: 'action.hover', borderRadius: 1 }}>
                    <Typography variant="body1" color="text.secondary">
                      SEO Health Chart (Placeholder)
                    </Typography>
                  </Box>
                </CardContent>
              </Card>
            </Grid>
          </Grid>
        </TabPanel>

        {/* Conversions Tab */}
        <TabPanel value={activeTab} index={3}>
          <Grid container spacing={3}>
            <Grid item xs={12} md={8}>
              <Box sx={{ height: '300px', display: 'flex', alignItems: 'center', justifyContent: 'center', bgcolor: 'action.hover', borderRadius: 1, mb: 3 }}>
                <Typography variant="h6" color="text.secondary">
                  Conversion Chart (Placeholder)
                </Typography>
              </Box>
            </Grid>
            <Grid item xs={12} md={4}>
              <Card sx={{ height: '100%' }}>
                <CardHeader title="Conversion Summary" />
                <CardContent>
                  <Box sx={{ mb: 2 }}>
                    <Typography variant="subtitle2" color="text.secondary">
                      Total Conversions
                    </Typography>
                    <Typography variant="h4">
                      138
                    </Typography>
                  </Box>
                  
                  <Box sx={{ mb: 2 }}>
                    <Typography variant="subtitle2" color="text.secondary">
                      Conversion Rate
                    </Typography>
                    <Typography variant="h4">
                      2.86%
                    </Typography>
                  </Box>
                  
                  <Box>
                    <Typography variant="subtitle2" color="text.secondary">
                      Revenue Generated
                    </Typography>
                    <Typography variant="h4">
                      $1,248.56
                    </Typography>
                  </Box>
                </CardContent>
              </Card>
            </Grid>
          </Grid>
        </TabPanel>
      </Paper>

      <Box sx={{ display: 'flex', justifyContent: 'flex-end' }}>
        <Button variant="outlined">
          Export Report
        </Button>
      </Box>
    </Box>
  );
}

export default Analytics;
