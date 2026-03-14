# AWS CloudFront Edge Functions - Study Guide

## Overview

This document covers **Customization at the Edge** in AWS, specifically focusing on CloudFront Edge Functions.

## What is Customization at the Edge?

Customization at the Edge refers to executing logic at CloudFront Edge locations before requests reach your main application. This approach minimizes latency by running code close to users globally.

## Edge Functions

**Edge Functions** are pieces of code that you write and attach to CloudFront distributions. They enable you to customize content delivery and add logic without managing servers.

### Types of Edge Functions

AWS CloudFront provides two types of Edge Functions:

1. **CloudFront Functions**
2. **Lambda@Edge**

Both are:
- **Serverless** - No server management required
- **Globally deployed** - Runs at Edge locations worldwide
- **Pay-per-use** - You only pay for what you use

## Use Cases

Edge Functions enable various customizations for modern applications:

### Security & Privacy
- Website security and privacy enhancements
- Bot mitigation at the Edge
- User authentication and authorization

### Performance & Optimization
- Dynamic web applications at the Edge
- Real-time image transformation
- Intelligent routing across origins and data centers

### User Experience
- Search Engine Optimization (SEO)
- A/B testing
- User prioritization
- User tracking and analytics

### Content Delivery
- Customize CDN content from CloudFront

## How CloudFront Functions Work

### Request Flow

1. **Viewer Request**: Client sends request to CloudFront
2. **Origin Request**: CloudFront forwards request to origin server
3. Edge Functions can intercept and modify requests at various points in this flow

## Key Benefits

- ✅ No server management
- ✅ Global deployment
- ✅ Minimal latency
- ✅ Cost-effective (pay-per-use)
- ✅ Fully serverless architecture

## Study Tips

- Understand the difference between CloudFront Functions and Lambda@Edge
- Know when to use Edge Functions vs. regional functions
- Practice identifying appropriate use cases for Edge customization
- Learn the request/response flow in CloudFront

## Important Concepts to Remember

- Edge Functions run **close to users** for minimal latency
- They attach to **CloudFront distributions**
- Two types: **CloudFront Functions** and **Lambda@Edge**
- Wide range of use cases from security to optimization
