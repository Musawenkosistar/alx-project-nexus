Project Nexus – Multi-Vendor Marketplace REST API
Overview

This project is a production-ready Multi-Vendor Marketplace REST API built using Django REST Framework.

It supports buyers, sellers, and admins with secure JWT authentication, optimized PostgreSQL database design, and Redis caching for performance enhancement.

This project demonstrates industry-level backend engineering practices including:

Clean architecture

Database normalization

Role-based access control

Transaction management

API documentation

Performance optimization

Tech Stack

Python 3.x

Django 4+

Django REST Framework

PostgreSQL

Redis

JWT (SimpleJWT)

drf-spectacular (Swagger Documentation)

Pytest

Docker (Planned)

Core Features
Authentication

JWT-based authentication

Access & Refresh tokens

Custom User model with roles:

Buyer

Seller

Admin

Product Management

Sellers can create, update, delete products

Category-based organization

Inventory tracking

Cached product listing

Order System

Buyers can place orders

Multiple products per order

Atomic transactions

Order status tracking

Reviews

Buyers can review purchased products

One review per product per user

Average rating calculation

Payments (Mocked)

Simulated payment endpoint

Updates order status

API Documentation

Swagger UI available at:

/api/docs/


Schema endpoint:

/api/schema/
