import React from 'react';
import { render, fireEvent, waitFor, screen  } from '@testing-library/react';
import App from './App';
import axios from 'axios';


jest.mock('axios');
describe('Initial Component Rendering', () => {
  beforeEach(() => {
    render(<App />);
  });

  it('renders the navbar with logo and navigation buttons', () => {
    expect(screen.getByAltText('logo')).toBeInTheDocument();
    expect(screen.getByText('Home')).toBeInTheDocument();
    expect(screen.getByText('About')).toBeInTheDocument();
  });

  it('renders the center-div with form elements', () => {
    expect(screen.getByPlaceholderText('Select File')).toBeInTheDocument();
    expect(screen.getByText('Upload')).toBeInTheDocument();
  });


  it('renders the instructions correctly', () => {
    expect(screen.getByText('Click on select file')).toBeInTheDocument();
    expect(screen.getByText('Chose the file you want to select')).toBeInTheDocument();
    expect(screen.getByText('Click on upload file')).toBeInTheDocument();
  });
});


describe('Select File functionality', () => {
  it('Slects file correctly', async () => {
    axios.post.mockResolvedValue({ data: { Status: 'ok', message: 'Player1,85%,Feedback1,Feedback2,Feedback3, Excellent' } });
    render(<App />);
    
    const file = new File(['video'], 'video.mp4', { type: 'video/mp4' });
    const input = screen.getByPlaceholderText('Select File');
    fireEvent.change(input, { target: { files: [file] } });

    await waitFor(() => {
      expect(screen.getByText('video.mp4')).toBeInTheDocument();
    });
  });

});



describe('Video Submission', () => {
  it('Analysing appears after video uplaod', async () => {
    axios.post.mockResolvedValue({ data: { Status: 'ok', message: 'Player1,85%,Feedback1,Feedback2,Feedback3, Excellent' } });
    render(<App />);
    
    const file = new File(['video'], 'video.mp4', { type: 'video/mp4' });
    const input = screen.getByPlaceholderText('Select File');
    fireEvent.change(input, { target: { files: [file] } });

    const uploadButton = screen.getByText('Upload');
    fireEvent.click(uploadButton);

    await waitFor(() => {
      expect(screen.getByText('Analysing...')).toBeInTheDocument();
    });
  });
  it('handles video submission correctly', async () => {
    axios.post.mockResolvedValue({ data: { Status: 'ok', message: 'Player1,85%,Feedback1,Feedback2,Feedback3, Excellent' } });
    render(<App />);
    
    const file = new File(['video'], 'video.mp4', { type: 'video/mp4' });
    const input = screen.getByPlaceholderText('Select File');
    fireEvent.change(input, { target: { files: [file] } });

    const uploadButton = screen.getByText('Upload');
    fireEvent.click(uploadButton);

    await waitFor(() => {
      expect(screen.getByText('Results')).toBeInTheDocument();
      expect(screen.getByText('Feedback1')).toBeInTheDocument();
    });
  });

});