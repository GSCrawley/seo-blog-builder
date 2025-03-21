import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Typography,
  Box,
  Paper,
  Stepper,
  Step,
  StepLabel,
  Button,
  TextField,
  MenuItem,
  FormControl,
  FormLabel,
  FormGroup,
  FormControlLabel,
  Checkbox,
  CircularProgress,
  Snackbar,
  Alert,
  Grid,
  Divider,
} from '@mui/material';
import { Formik, Form, Field } from 'formik';
import * as Yup from 'yup';
import { createBlog } from '../services/blogService';
import { handleApiError } from '../utils/apiUtils';

// Step components
const TopicStep = ({ formik }) => (
  <Box sx={{ mt: 2 }}>
    <Typography variant="h6" gutterBottom>
      What is your blog topic?
    </Typography>
    <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
      Enter a specific topic for your blog. Be as descriptive as possible to get the best results.
    </Typography>
    <TextField
      fullWidth
      label="Blog Topic"
      name="topic"
      variant="outlined"
      value={formik.values.topic}
      onChange={formik.handleChange}
      error={formik.touched.topic && Boolean(formik.errors.topic)}
      helperText={formik.touched.topic && formik.errors.topic}
      placeholder="e.g. Fitness tips for busy professionals"
      sx={{ mb: 2 }}
    />
    <TextField
      fullWidth
      label="Industry"
      name="industry"
      select
      variant="outlined"
      value={formik.values.industry}
      onChange={formik.handleChange}
      error={formik.touched.industry && Boolean(formik.errors.industry)}
      helperText={formik.touched.industry && formik.errors.industry}
    >
      <MenuItem value="health_fitness">Health & Fitness</MenuItem>
      <MenuItem value="finance">Finance & Money</MenuItem>
      <MenuItem value="technology">Technology</MenuItem>
      <MenuItem value="travel">Travel</MenuItem>
      <MenuItem value="food">Food & Cooking</MenuItem>
      <MenuItem value="business">Business</MenuItem>
      <MenuItem value="marketing">Marketing</MenuItem>
      <MenuItem value="education">Education</MenuItem>
      <MenuItem value="lifestyle">Lifestyle</MenuItem>
      <MenuItem value="other">Other</MenuItem>
    </TextField>
  </Box>
);

const AudienceStep = ({ formik }) => (
  <Box sx={{ mt: 2 }}>
    <Typography variant="h6" gutterBottom>
      Who is your target audience?
    </Typography>
    <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
      Define your target audience to create content that resonates with them.
    </Typography>
    <TextField
      fullWidth
      label="Target Audience Description"
      name="targetAudience"
      variant="outlined"
      value={formik.values.targetAudience}
      onChange={formik.handleChange}
      error={formik.touched.targetAudience && Boolean(formik.errors.targetAudience)}
      helperText={formik.touched.targetAudience && formik.errors.targetAudience}
      placeholder="e.g. Professionals aged 25-40 who want to stay fit despite a busy schedule"
      multiline
      rows={3}
      sx={{ mb: 2 }}
    />
    <FormControl component="fieldset" sx={{ mt: 2 }}>
      <FormLabel component="legend">Audience Characteristics</FormLabel>
      <FormGroup>
        <Grid container spacing={2}>
          <Grid item xs={6}>
            <FormControlLabel
              control={
                <Field
                  as={Checkbox}
                  name="audienceTraits"
                  value="beginners"
                  checked={formik.values.audienceTraits.includes('beginners')}
                  onChange={formik.handleChange}
                />
              }
              label="Beginners"
            />
          </Grid>
          <Grid item xs={6}>
            <FormControlLabel
              control={
                <Field
                  as={Checkbox}
                  name="audienceTraits"
                  value="intermediates"
                  checked={formik.values.audienceTraits.includes('intermediates')}
                  onChange={formik.handleChange}
                />
              }
              label="Intermediates"
            />
          </Grid>
          <Grid item xs={6}>
            <FormControlLabel
              control={
                <Field
                  as={Checkbox}
                  name="audienceTraits"
                  value="experts"
                  checked={formik.values.audienceTraits.includes('experts')}
                  onChange={formik.handleChange}
                />
              }
              label="Experts"
            />
          </Grid>
          <Grid item xs={6}>
            <FormControlLabel
              control={
                <Field
                  as={Checkbox}
                  name="audienceTraits"
                  value="professionals"
                  checked={formik.values.audienceTraits.includes('professionals')}
                  onChange={formik.handleChange}
                />
              }
              label="Professionals"
            />
          </Grid>
        </Grid>
      </FormGroup>
    </FormControl>
  </Box>
);

const ContentStep = ({ formik }) => (
  <Box sx={{ mt: 2 }}>
    <Typography variant="h6" gutterBottom>
      Content Preferences
    </Typography>
    <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
      Customize how your blog content will be structured and presented.
    </Typography>
    <TextField
      fullWidth
      label="Number of Articles"
      name="numArticles"
      type="number"
      variant="outlined"
      InputProps={{ inputProps: { min: 1, max: 20 } }}
      value={formik.values.numArticles}
      onChange={formik.handleChange}
      error={formik.touched.numArticles && Boolean(formik.errors.numArticles)}
      helperText={formik.touched.numArticles && formik.errors.numArticles}
      sx={{ mb: 2 }}
    />
    <TextField
      fullWidth
      label="Content Tone"
      name="contentTone"
      select
      variant="outlined"
      value={formik.values.contentTone}
      onChange={formik.handleChange}
      error={formik.touched.contentTone && Boolean(formik.errors.contentTone)}
      helperText={formik.touched.contentTone && formik.errors.contentTone}
      sx={{ mb: 2 }}
    >
      <MenuItem value="professional">Professional</MenuItem>
      <MenuItem value="conversational">Conversational</MenuItem>
      <MenuItem value="educational">Educational</MenuItem>
      <MenuItem value="entertaining">Entertaining</MenuItem>
      <MenuItem value="persuasive">Persuasive</MenuItem>
    </TextField>
    <FormControl component="fieldset" sx={{ mt: 2 }}>
      <FormLabel component="legend">Content Types</FormLabel>
      <FormGroup>
        <Grid container spacing={2}>
          <Grid item xs={6}>
            <FormControlLabel
              control={
                <Field
                  as={Checkbox}
                  name="contentTypes"
                  value="how_to"
                  checked={formik.values.contentTypes.includes('how_to')}
                  onChange={formik.handleChange}
                />
              }
              label="How-to Guides"
            />
          </Grid>
          <Grid item xs={6}>
            <FormControlLabel
              control={
                <Field
                  as={Checkbox}
                  name="contentTypes"
                  value="listicles"
                  checked={formik.values.contentTypes.includes('listicles')}
                  onChange={formik.handleChange}
                />
              }
              label="Listicles"
            />
          </Grid>
          <Grid item xs={6}>
            <FormControlLabel
              control={
                <Field
                  as={Checkbox}
                  name="contentTypes"
                  value="reviews"
                  checked={formik.values.contentTypes.includes('reviews')}
                  onChange={formik.handleChange}
                />
              }
              label="Reviews"
            />
          </Grid>
          <Grid item xs={6}>
            <FormControlLabel
              control={
                <Field
                  as={Checkbox}
                  name="contentTypes"
                  value="comparisons"
                  checked={formik.values.contentTypes.includes('comparisons')}
                  onChange={formik.handleChange}
                />
              }
              label="Comparisons"
            />
          </Grid>
        </Grid>
      </FormGroup>
    </FormControl>
  </Box>
);

const MonetizationStep = ({ formik }) => (
  <Box sx={{ mt: 2 }}>
    <Typography variant="h6" gutterBottom>
      Monetization Strategy
    </Typography>
    <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
      Choose how you want to monetize your blog content.
    </Typography>
    <TextField
      fullWidth
      label="Primary Monetization Method"
      name="monetizationMethod"
      select
      variant="outlined"
      value={formik.values.monetizationMethod}
      onChange={formik.handleChange}
      error={formik.touched.monetizationMethod && Boolean(formik.errors.monetizationMethod)}
      helperText={formik.touched.monetizationMethod && formik.errors.monetizationMethod}
      sx={{ mb: 2 }}
    >
      <MenuItem value="affiliate">Affiliate Marketing</MenuItem>
      <MenuItem value="ads">Display Advertising</MenuItem>
      <MenuItem value="products">Digital Products</MenuItem>
      <MenuItem value="services">Services</MenuItem>
      <MenuItem value="none">None</MenuItem>
    </TextField>

    {formik.values.monetizationMethod === 'affiliate' && (
      <TextField
        fullWidth
        label="Affiliate Programs/Products (optional)"
        name="affiliateProducts"
        variant="outlined"
        multiline
        rows={3}
        value={formik.values.affiliateProducts}
        onChange={formik.handleChange}
        placeholder="e.g. Amazon Associates, Fitness equipment, Nutrition supplements"
        sx={{ mb: 2 }}
      />
    )}

    <FormControl component="fieldset" sx={{ mt: 2 }}>
      <FormLabel component="legend">Additional Monetization Features</FormLabel>
      <FormGroup>
        <Grid container spacing={2}>
          <Grid item xs={6}>
            <FormControlLabel
              control={
                <Field
                  as={Checkbox}
                  name="monetizationFeatures"
                  value="email_capture"
                  checked={formik.values.monetizationFeatures.includes('email_capture')}
                  onChange={formik.handleChange}
                />
              }
              label="Email Capture"
            />
          </Grid>
          <Grid item xs={6}>
            <FormControlLabel
              control={
                <Field
                  as={Checkbox}
                  name="monetizationFeatures"
                  value="product_reviews"
                  checked={formik.values.monetizationFeatures.includes('product_reviews')}
                  onChange={formik.handleChange}
                />
              }
              label="Product Reviews"
            />
          </Grid>
          <Grid item xs={6}>
            <FormControlLabel
              control={
                <Field
                  as={Checkbox}
                  name="monetizationFeatures"
                  value="comparison_tables"
                  checked={formik.values.monetizationFeatures.includes('comparison_tables')}
                  onChange={formik.handleChange}
                />
              }
              label="Comparison Tables"
            />
          </Grid>
          <Grid item xs={6}>
            <FormControlLabel
              control={
                <Field
                  as={Checkbox}
                  name="monetizationFeatures"
                  value="resource_pages"
                  checked={formik.values.monetizationFeatures.includes('resource_pages')}
                  onChange={formik.handleChange}
                />
              }
              label="Resource Pages"
            />
          </Grid>
        </Grid>
      </FormGroup>
    </FormControl>
  </Box>
);

// Validation Schema
const validationSchema = Yup.object({
  topic: Yup.string().required('Topic is required'),
  industry: Yup.string().required('Industry is required'),
  targetAudience: Yup.string().required('Target audience is required'),
  numArticles: Yup.number()
    .required('Number of articles is required')
    .min(1, 'Minimum 1 article')
    .max(20, 'Maximum 20 articles'),
  contentTone: Yup.string().required('Content tone is required'),
  monetizationMethod: Yup.string().required('Monetization method is required'),
});

// Main component
function BlogGenerator() {
  const [activeStep, setActiveStep] = useState(0);
  const [snackbar, setSnackbar] = useState({
    open: false,
    message: '',
    severity: 'success',
  });
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const steps = ['Topic', 'Audience', 'Content', 'Monetization'];

  const handleNext = () => {
    setActiveStep((prevActiveStep) => prevActiveStep + 1);
  };

  const handleBack = () => {
    setActiveStep((prevActiveStep) => prevActiveStep - 1);
  };

  const handleCloseSnackbar = () => {
    setSnackbar({ ...snackbar, open: false });
  };

  const handleSubmit = async (values) => {
    setLoading(true);
    
    try {
      // Transform form values to match API expectations
      const blogData = {
        topic: values.topic,
        preferences: {
          industry: values.industry,
          target_audience: values.targetAudience,
          audience_traits: values.audienceTraits,
          num_articles: Number(values.numArticles),
          content_tone: values.contentTone,
          content_types: values.contentTypes,
          monetization_method: values.monetizationMethod,
          monetization_features: values.monetizationFeatures,
          affiliate_products: values.affiliateProducts || '',
        }
      };
      
      const response = await createBlog(blogData);
      
      setSnackbar({
        open: true,
        message: 'Blog generation started successfully!',
        severity: 'success',
      });
      
      // Navigate to the status page with the project ID
      navigate(`/blog-status/${response.project_id}`);
    } catch (error) {
      // Use our utility function to handle the error
      const errorMessage = error.message || 'Failed to start blog generation. Please try again.';
      
      setSnackbar({
        open: true,
        message: errorMessage,
        severity: 'error',
      });
      setLoading(false);
    }
  };

  const renderStepContent = (step, formik) => {
    switch (step) {
      case 0:
        return <TopicStep formik={formik} />;
      case 1:
        return <AudienceStep formik={formik} />;
      case 2:
        return <ContentStep formik={formik} />;
      case 3:
        return <MonetizationStep formik={formik} />;
      default:
        return null;
    }
  };

  return (
    <Box>
      <Typography variant="h4" component="h1" gutterBottom>
        Blog Generator
      </Typography>
      <Typography variant="body1" color="text.secondary" sx={{ mb: 3 }}>
        Generate a complete, SEO-optimized blog with just a few clicks.
      </Typography>

      <Paper sx={{ p: 3, mb: 3 }}>
        <Stepper activeStep={activeStep} sx={{ mb: 3 }}>
          {steps.map((label) => (
            <Step key={label}>
              <StepLabel>{label}</StepLabel>
            </Step>
          ))}
        </Stepper>

        <Divider sx={{ mb: 3 }} />

        <Formik
          initialValues={{
            topic: '',
            industry: '',
            targetAudience: '',
            audienceTraits: [],
            numArticles: 5,
            contentTone: 'professional',
            contentTypes: ['how_to', 'listicles'],
            monetizationMethod: 'affiliate',
            monetizationFeatures: ['email_capture'],
            affiliateProducts: '',
          }}
          validationSchema={validationSchema}
          onSubmit={handleSubmit}
        >
          {(formik) => (
            <Form>
              {renderStepContent(activeStep, formik)}

              <Box sx={{ display: 'flex', justifyContent: 'space-between', mt: 4 }}>
                <Button
                  disabled={activeStep === 0 || loading}
                  onClick={handleBack}
                  variant="outlined"
                >
                  Back
                </Button>
                <Box>
                  {activeStep === steps.length - 1 ? (
                    <Button
                      disabled={!formik.isValid || loading}
                      type="submit"
                      variant="contained"
                      color="primary"
                      startIcon={loading && <CircularProgress size={24} color="inherit" />}
                    >
                      {loading ? 'Generating...' : 'Generate Blog'}
                    </Button>
                  ) : (
                    <Button
                      variant="contained"
                      color="primary"
                      onClick={() => {
                        formik.validateForm().then((errors) => {
                          // Only proceed if the current step fields are valid
                          const currentStepValid = (() => {
                            switch (activeStep) {
                              case 0:
                                return !errors.topic && !errors.industry;
                              case 1:
                                return !errors.targetAudience;
                              case 2:
                                return !errors.numArticles && !errors.contentTone;
                              default:
                                return true;
                            }
                          })();

                          if (currentStepValid) {
                            handleNext();
                          } else {
                            // Touch the fields to show errors
                            switch (activeStep) {
                              case 0:
                                formik.setTouched({ topic: true, industry: true });
                                break;
                              case 1:
                                formik.setTouched({ targetAudience: true });
                                break;
                              case 2:
                                formik.setTouched({ numArticles: true, contentTone: true });
                                break;
                              default:
                                break;
                            }
                          }
                        });
                      }}
                    >
                      Next
                    </Button>
                  )}
                </Box>
              </Box>
            </Form>
          )}
        </Formik>
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

export default BlogGenerator;
