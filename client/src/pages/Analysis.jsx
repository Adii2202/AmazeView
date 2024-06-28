import React, { useState } from "react";
import ChartComponent from "../components/dashboard/LDA";
import {
  Box,
  Typography,
  Card,
  CardContent,
  CardMedia,
  List,
  ListItem,
  ListItemText,
  Grid,
  Button,
  Menu,
  MenuItem,
} from "@mui/material";
import PhotoCamera from "@mui/icons-material/PhotoCamera";
import Videocam from "@mui/icons-material/Videocam";
import Carousel from "react-material-ui-carousel";

const Analysis = () => {
  const [anchorEl, setAnchorEl] = useState(null);
  const [uploadedFiles, setUploadedFiles] = useState({
    images: [],
    videos: [],
  });
  const [counterfeitingDetected, setCounterfeitingDetected] = useState(false);

  const handleClick = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  const handleFileUpload = (event) => {
    const files = Array.from(event.target.files);
    const newFiles = files.map((file) => ({
      type: file.type.startsWith("image/") ? "image" : "video",
      url: URL.createObjectURL(file),
    }));

    setUploadedFiles((prevFiles) => ({
      ...prevFiles,
      images: prevFiles.images.concat(
        newFiles.filter((file) => file.type === "image")
      ),
      videos: prevFiles.videos.concat(
        newFiles.filter((file) => file.type === "video")
      ),
    }));

    // Simulate detection logic (replace with actual detection logic if available)
    simulateDetection(newFiles);
  };

  const simulateDetection = (files) => {
    // Simulate detection logic here based on uploaded files
    const isCounterfeit = files.some((file) => {
      // Simulate by checking file properties or using AI/ML model
      return file.type === "image" && file.url.includes("placeholder");
    });

    // Update counterfeiting detection status
    setCounterfeitingDetected(isCounterfeit);
  };

  const product = {
    images: [
      "https://m.media-amazon.com/images/I/71Z+MJyYIGL.jpg",
      "https://m.media-amazon.com/images/I/71RBRuw9EUL.jpg",
      "https://m.media-amazon.com/images/I/71k0rtXXitL.jpg",
      "https://m.media-amazon.com/images/I/715eH4s5CvL.jpg",
    ],
    videos: [
      "https://www.example.com/video.mp4",
      "https://www.example.com/video.mp4",
    ],
    counterfeitDetected: true, // Set to false if no counterfeiting detected
    description: "No rider would be assigned.",
    fakeReviews: [
      "Great Work Going",
      "Subsribe to our channel for more such videos",
      "value money Best toothpaste 😁😁😁 Reason always bought hate mint Verry fast delivery & lower price segment cheaper offline market way quality awesome much effective & purely natural Good usfull Good fresh feeling clean teeth.",
      "Feel safe teeth.",
    ],
  };

  return (
    <Box sx={{ maxWidth: 800, margin: "auto", padding: 4 }}>
      <Box sx={{ display: "flex", justifyContent: "flex-end", mb: 2 }}>
        <Button variant="contained" onClick={handleClick}>
          Upload Images/Videos
        </Button>
        <Menu
          anchorEl={anchorEl}
          open={Boolean(anchorEl)}
          onClose={handleClose}
        >
          <MenuItem>
            <label htmlFor="upload-image" style={{ display: "block" }}>
              Upload Images
              <input
                accept="image/*"
                style={{ display: "none" }}
                id="upload-image"
                type="file"
                multiple
                onChange={handleFileUpload}
              />
            </label>
          </MenuItem>
          <MenuItem>
            <label htmlFor="upload-video" style={{ display: "block" }}>
              Upload Videos
              <input
                accept="video/*"
                style={{ display: "none" }}
                id="upload-video"
                type="file"
                multiple
                onChange={handleFileUpload}
              />
            </label>
          </MenuItem>
        </Menu>
      </Box>

      {counterfeitingDetected && (
        <Card sx={{ marginBottom: 4 }}>
          <CardContent>
            <Typography variant="body1" color="error" gutterBottom>
              Counterfeiting detected in this product.
            </Typography>
            <Typography variant="body2" color="text.secondary" paragraph>
              Therefore, no rider will be assigned for picking this product.
            </Typography>
          </CardContent>
        </Card>
      )}

      <Typography variant="h4" component="h1" gutterBottom>
        Product Analysis
      </Typography>
      <Card sx={{ marginBottom: 4 }}>
        <CardContent>
          <Typography variant="h6" component="h2">
            Counterfeiting Detected:{" "}
            {product.counterfeitDetected ? "Yes" : "No"}
          </Typography>
          <Typography variant="body2" color="text.secondary" paragraph>
            {product.description}
          </Typography>
        </CardContent>
      </Card>

      <Grid container spacing={2}>
        <Grid item xs={12} sm={6}>
          <Card sx={{ marginBottom: 4 }}>
            <CardContent>
              <Typography variant="h6" component="h2" gutterBottom>
                Images
              </Typography>
              <Carousel animation="slide" timeout={500} navButtonsAlwaysVisible>
                {[...product.images, ...uploadedFiles.images].map(
                  (image, index) => (
                    <CardMedia
                      key={index}
                      component="img"
                      image={image}
                      alt={`Image ${index + 1}`}
                    />
                  )
                )}
              </Carousel>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6}>
          <Card sx={{ marginBottom: 4 }}>
            <CardContent>
              <Typography variant="h6" component="h2" gutterBottom>
                Videos
              </Typography>
              <Carousel animation="slide" timeout={500} navButtonsAlwaysVisible>
                {[...product.videos, ...uploadedFiles.videos].map(
                  (video, index) => (
                    <CardMedia
                      key={index}
                      component="video"
                      src={video}
                      controls
                    />
                  )
                )}
              </Carousel>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      <Card sx={{ marginBottom: 4 }}>
        <CardContent>
          <Typography variant="h6" component="h2">
            Fake Reviews
          </Typography>
          <List>
            {product.fakeReviews.map((review, index) => (
              <ListItem key={index}>
                <ListItemText primary={review} />
              </ListItem>
            ))}
          </List>
        </CardContent>
      </Card>

      <Card>
        <CardContent>
          <Typography variant="h6" component="h2">
            Fake Reviews Analysis
          </Typography>
          <Box sx={{ height: 400 }}>
            <ChartComponent />
          </Box>
        </CardContent>
      </Card>
    </Box>
  );
};

export default Analysis;
