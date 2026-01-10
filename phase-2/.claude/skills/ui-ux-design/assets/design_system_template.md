# Design System Template

## Color Palette

### Primary Colors
- **Primary**: `#007BFF` (Blue) - Primary actions and highlights
- **Primary Dark**: `#0056b3` - Hover states and active elements
- **Primary Light**: `#e7f3ff` - Backgrounds and subtle elements

### Secondary Colors
- **Secondary**: `#6c757d` (Gray) - Secondary actions and text
- **Secondary Dark**: `#495057` - Emphasized secondary elements
- **Secondary Light**: `#f8f9fa` - Backgrounds and subtle elements

### Status Colors
- **Success**: `#28a745` - Positive actions and feedback
- **Warning**: `#ffc107` - Cautions and warnings
- **Error**: `#dc3545` - Errors and destructive actions
- **Info**: `#17a2b8` - Informational elements

### Neutral Colors
- **Black**: `#000000` - Primary text
- **Dark Gray**: `#343a40` - Secondary text
- **Medium Gray**: `#6c757d` - Disabled elements
- **Light Gray**: `#e9ecef` - Borders and dividers
- **White**: `#ffffff` - Backgrounds

## Typography

### Font Families
- **Primary Font**: Inter, system-ui, -apple-system, sans-serif
- **Secondary Font**: Source Code Pro, monospace (for code elements)

### Typography Scale
- **Display**: 48px (weight: 700) - Hero headings
- **H1**: 36px (weight: 700) - Primary page headings
- **H2**: 32px (weight: 700) - Section headings
- **H3**: 28px (weight: 700) - Subsection headings
- **H4**: 24px (weight: 600) - Component headings
- **H5**: 20px (weight: 600) - Subtle headings
- **H6**: 16px (weight: 600) - Minor headings
- **Body Large**: 18px (weight: 400) - Long-form content
- **Body**: 16px (weight: 400) - Standard content
- **Body Small**: 14px (weight: 400) - Secondary content
- **Caption**: 12px (weight: 400) - Supporting text

### Line Height
- **Display**: 1.2
- **Headings**: 1.3
- **Body Large**: 1.5
- **Body**: 1.5
- **Body Small**: 1.4
- **Caption**: 1.3

## Spacing System

### Grid System
- **Base Unit**: 8px
- **Scale**: 2px, 4px, 8px, 12px, 16px, 24px, 32px, 48px, 64px, 80px, 96px

### Component Spacing
- **Padding Small**: 8px
- **Padding Medium**: 16px
- **Padding Large**: 24px
- **Padding XL**: 32px
- **Margin Small**: 4px
- **Margin Medium**: 16px
- **Margin Large**: 24px
- **Margin XL**: 40px

## Component Specifications

### Button Component
- **Small**: 32px height, 12px horizontal padding
- **Medium**: 40px height, 16px horizontal padding
- **Large**: 48px height, 24px horizontal padding
- **Border Radius**: 4px
- **Primary States**:
  - Default: Primary color, white text
  - Hover: Primary Dark, white text
  - Active: Primary Dark, white text
  - Disabled: Light Gray, Medium Gray text

### Input Component
- **Height**: 40px
- **Border Radius**: 4px
- **Border**: 1px solid Light Gray
- **Focus**: 2px solid Primary with 2px transparent offset
- **Padding**: 0 12px
- **Placeholder**: Medium Gray, 400 weight

### Card Component
- **Border Radius**: 8px
- **Border**: 1px solid rgba(0,0,0,0.1)
- **Shadow**: 0 2px 8px rgba(0,0,0,0.1)
- **Padding**: 16px
- **Background**: White

## Breakpoints

### Responsive Breakpoints
- **Mobile**: 0px - 767px
- **Tablet**: 768px - 1023px
- **Desktop**: 1024px - 1439px
- **Large Desktop**: 1440px+

## Accessibility Standards

### Color Contrast
- **Text/Background**: Minimum 4.5:1 ratio
- **Large Text**: Minimum 3:1 ratio
- **UI Elements**: Minimum 3:1 ratio

### Touch Target Size
- **Minimum**: 44px by 44px
- **Recommended**: 48px by 48px

## Icons

### Icon Sizes
- **Small**: 16px
- **Medium**: 20px
- **Large**: 24px
- **Extra Large**: 32px

### Icon Library
- **Primary**: Feather Icons or similar simple icon set
- **Alternative**: Material Icons for more complex needs