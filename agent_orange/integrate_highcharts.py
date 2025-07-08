#!/usr/bin/env python3
"""
Integrate Highcharts with extracted Cloudscape materials
Creates a unified design system with charts that match your original design
"""

import shutil
import os
from pathlib import Path
import re
from bs4 import BeautifulSoup

class HighchartsCloudscapeIntegrator:
    def __init__(self):
        self.cloudscape_dir = Path("refined_materials/cloudscape_complete")
        self.highcharts_dir = Path("highcharts")
        self.output_dir = Path("refined_materials/integrated_design_system")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def integrate_all(self):
        """Complete integration of Highcharts with Cloudscape"""
        print("🔶 Integrating Highcharts with Cloudscape Design System")
        print()
        
        # 1. Copy Cloudscape materials
        self.copy_cloudscape_materials()
        
        # 2. Copy Highcharts assets
        self.copy_highcharts_assets()
        
        # 3. Create design token mappings
        self.create_design_token_integration()
        
        # 4. Create example pages
        self.create_integrated_examples()
        
        # 5. Build CSS theme integration
        self.create_cloudscape_highcharts_theme()
        
        print("✅ Integration complete!")
        print(f"📁 Check {self.output_dir} for the integrated design system")

    def copy_cloudscape_materials(self):
        """Copy Cloudscape CSS, SCSS, and examples"""
        print("📋 Copying Cloudscape materials...")
        
        # Copy CSS files
        if (self.cloudscape_dir / "css").exists():
            shutil.copytree(
                self.cloudscape_dir / "css", 
                self.output_dir / "css" / "cloudscape",
                dirs_exist_ok=True
            )
        
        # Copy SCSS source files
        if (self.cloudscape_dir / "github_css").exists():
            shutil.copytree(
                self.cloudscape_dir / "github_css",
                self.output_dir / "scss" / "cloudscape",
                dirs_exist_ok=True
            )
        
        # Copy HTML examples
        html_files = list(self.cloudscape_dir.glob("*.html"))
        examples_dir = self.output_dir / "examples" / "cloudscape"
        examples_dir.mkdir(parents=True, exist_ok=True)
        
        for html_file in html_files:
            shutil.copy2(html_file, examples_dir)
        
        print(f"✅ Copied {len(html_files)} HTML examples and CSS/SCSS files")

    def copy_highcharts_assets(self):
        """Copy Highcharts CSS, themes, and core files"""
        print("📊 Copying Highcharts assets...")
        
        # Copy CSS files
        if (self.highcharts_dir / "css").exists():
            shutil.copytree(
                self.highcharts_dir / "css",
                self.output_dir / "css" / "highcharts",
                dirs_exist_ok=True
            )
        
        # Copy built JavaScript files (look for code directory)
        if (self.highcharts_dir / "code").exists():
            shutil.copytree(
                self.highcharts_dir / "code",
                self.output_dir / "js" / "highcharts",
                dirs_exist_ok=True
            )
        
        # Copy TypeScript source files for reference
        if (self.highcharts_dir / "ts").exists():
            shutil.copytree(
                self.highcharts_dir / "ts",
                self.output_dir / "src" / "highcharts-ts",
                dirs_exist_ok=True
            )
        
        print("✅ Copied Highcharts CSS, themes, and source files")

    def create_design_token_integration(self):
        """Create design token mappings between Cloudscape and Highcharts"""
        print("🎨 Creating design token integration...")
        
        # Read Cloudscape SCSS to extract design tokens
        cloudscape_tokens = self.extract_cloudscape_tokens()
        
        # Read Highcharts CSS to extract color variables
        highcharts_tokens = self.extract_highcharts_tokens()
        
        # Create integration CSS
        integration_css = self.create_token_mapping_css(cloudscape_tokens, highcharts_tokens)
        
        # Save integration file
        integration_file = self.output_dir / "css" / "cloudscape-highcharts-integration.css"
        with open(integration_file, 'w', encoding='utf-8') as f:
            f.write(integration_css)
        
        print(f"✅ Created design token integration: {integration_file}")

    def extract_cloudscape_tokens(self):
        """Extract design tokens from Cloudscape SCSS files"""
        tokens = {}
        scss_dir = self.output_dir / "scss" / "cloudscape"
        
        if not scss_dir.exists():
            return tokens
        
        for scss_file in scss_dir.rglob("*.scss"):
            try:
                with open(scss_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # Look for CSS variables and SCSS variables
                css_vars = re.findall(r'--[\w-]+:\s*([^;]+)', content)
                scss_vars = re.findall(r'\$[\w-]+:\s*([^;]+)', content)
                awsui_usage = re.findall(r'awsui\.\$[\w-]+', content)
                
                if css_vars or scss_vars or awsui_usage:
                    tokens[scss_file.name] = {
                        'css_vars': css_vars,
                        'scss_vars': scss_vars,
                        'awsui_tokens': awsui_usage
                    }
            except Exception as e:
                continue
        
        return tokens

    def extract_highcharts_tokens(self):
        """Extract color and styling tokens from Highcharts CSS"""
        tokens = {}
        highcharts_css = self.highcharts_dir / "css" / "highcharts.css"
        
        if highcharts_css.exists():
            with open(highcharts_css, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Extract CSS custom properties
            css_vars = re.findall(r'(--highcharts-[\w-]+):\s*([^;]+)', content)
            tokens['highcharts'] = dict(css_vars)
        
        return tokens

    def create_token_mapping_css(self, cloudscape_tokens, highcharts_tokens):
        """Create CSS that maps Cloudscape design tokens to Highcharts"""
        css = """/*
 * Cloudscape + Highcharts Design Token Integration
 * Maps Cloudscape design tokens to Highcharts styling variables
 */

:root {
    /* Cloudscape-inspired Highcharts color palette */
    --highcharts-color-0: #0972d3;  /* Primary blue */
    --highcharts-color-1: #5f636e;  /* Neutral gray */
    --highcharts-color-2: #0e8238;  /* Success green */
    --highcharts-color-3: #df4020;  /* Error red */
    --highcharts-color-4: #8c4fff;  /* Purple accent */
    --highcharts-color-5: #ff8800;  /* Warning orange */
    --highcharts-color-6: #0070ba;  /* Info blue */
    --highcharts-color-7: #d91515;  /* Alert red */
    --highcharts-color-8: #b45a00;  /* Dark orange */
    --highcharts-color-9: #7a7a7a;  /* Muted gray */

    /* Background colors matching Cloudscape */
    --highcharts-background-color: #ffffff;
    --highcharts-plot-background-color: #fafbfc;
    
    /* Text colors from Cloudscape neutral palette */
    --highcharts-neutral-color-100: #16191f;  /* Strong text */
    --highcharts-neutral-color-80: #5f636e;   /* Main text */
    --highcharts-neutral-color-60: #879596;   /* Muted text */
    --highcharts-neutral-color-40: #aeb6b7;   /* Disabled text */
    --highcharts-neutral-color-20: #d5dbdb;   /* Light borders */
    --highcharts-neutral-color-10: #eaeded;   /* Grid lines */
    --highcharts-neutral-color-5: #f2f3f3;    /* Subtle backgrounds */
}

/* Dark mode variant */
.highcharts-dark {
    --highcharts-background-color: #16191f;
    --highcharts-plot-background-color: #1d2125;
    --highcharts-neutral-color-100: #ffffff;
    --highcharts-neutral-color-80: #d5dbdb;
    --highcharts-neutral-color-60: #aeb6b7;
    --highcharts-neutral-color-40: #879596;
    --highcharts-neutral-color-20: #5f636e;
    --highcharts-neutral-color-10: #414b53;
    --highcharts-neutral-color-5: #2a3238;
}

/* Cloudscape component integration styles */
.cloudscape-chart-container {
    background: var(--highcharts-background-color);
    border: 1px solid var(--highcharts-neutral-color-20);
    border-radius: 8px;
    padding: 16px;
    margin: 16px 0;
}

.cloudscape-chart-title {
    color: var(--highcharts-neutral-color-100);
    font-size: 18px;
    font-weight: 600;
    margin-bottom: 12px;
}

.cloudscape-chart-description {
    color: var(--highcharts-neutral-color-80);
    font-size: 14px;
    margin-bottom: 16px;
}

/* Highcharts-specific Cloudscape styling */
.highcharts-container {
    font-family: "Amazon Ember", "Helvetica Neue", Roboto, Arial, sans-serif;
}

.highcharts-title {
    color: var(--highcharts-neutral-color-100) !important;
    font-weight: 700 !important;
}

.highcharts-subtitle {
    color: var(--highcharts-neutral-color-80) !important;
    font-weight: 400 !important;
}

.highcharts-axis-labels text {
    color: var(--highcharts-neutral-color-80) !important;
    font-size: 12px !important;
}

.highcharts-legend-item text {
    color: var(--highcharts-neutral-color-80) !important;
    font-size: 12px !important;
}

.highcharts-tooltip-box {
    stroke: var(--highcharts-neutral-color-20) !important;
    fill: var(--highcharts-background-color) !important;
}

.highcharts-grid-line {
    stroke: var(--highcharts-neutral-color-10) !important;
}"""

        return css

    def create_cloudscape_highcharts_theme(self):
        """Create a complete Highcharts theme that matches Cloudscape"""
        print("🎨 Creating Cloudscape Highcharts theme...")
        
        theme_js = """/*
 * Cloudscape Design System Theme for Highcharts
 * Matches AWS Cloudscape visual design language
 */

Highcharts.theme = {
    colors: [
        '#0972d3', // Primary blue
        '#5f636e', // Neutral gray  
        '#0e8238', // Success green
        '#df4020', // Error red
        '#8c4fff', // Purple accent
        '#ff8800', // Warning orange
        '#0070ba', // Info blue
        '#d91515', // Alert red
        '#b45a00', // Dark orange
        '#7a7a7a'  // Muted gray
    ],
    
    chart: {
        backgroundColor: '#ffffff',
        style: {
            fontFamily: '"Amazon Ember", "Helvetica Neue", Roboto, Arial, sans-serif',
            fontSize: '14px'
        },
        plotBorderColor: '#eaeded',
        plotBackgroundColor: '#fafbfc'
    },
    
    title: {
        style: {
            color: '#16191f',
            fontSize: '18px',
            fontWeight: '700'
        }
    },
    
    subtitle: {
        style: {
            color: '#5f636e',
            fontSize: '14px',
            fontWeight: '400'
        }
    },
    
    xAxis: {
        gridLineColor: '#eaeded',
        lineColor: '#d5dbdb',
        minorGridLineColor: '#f2f3f3',
        tickColor: '#d5dbdb',
        title: {
            style: {
                color: '#5f636e',
                fontSize: '12px',
                fontWeight: '600'
            }
        },
        labels: {
            style: {
                color: '#5f636e',
                fontSize: '12px'
            }
        }
    },
    
    yAxis: {
        gridLineColor: '#eaeded',
        lineColor: '#d5dbdb',
        minorGridLineColor: '#f2f3f3',
        tickColor: '#d5dbdb',
        title: {
            style: {
                color: '#5f636e',
                fontSize: '12px',
                fontWeight: '600'
            }
        },
        labels: {
            style: {
                color: '#5f636e',
                fontSize: '12px'
            }
        }
    },
    
    legend: {
        itemStyle: {
            color: '#5f636e',
            fontSize: '12px',
            fontWeight: '400'
        },
        itemHoverStyle: {
            color: '#16191f'
        },
        itemHiddenStyle: {
            color: '#aeb6b7'
        }
    },
    
    tooltip: {
        backgroundColor: '#ffffff',
        borderColor: '#d5dbdb',
        borderRadius: 8,
        shadow: {
            color: 'rgba(22, 25, 31, 0.1)',
            offsetX: 0,
            offsetY: 2,
            opacity: 0.15,
            width: 8
        },
        style: {
            color: '#16191f',
            fontSize: '12px'
        }
    },
    
    plotOptions: {
        series: {
            borderWidth: 0,
            borderRadius: 2
        },
        column: {
            borderRadius: 2
        },
        bar: {
            borderRadius: 2
        }
    },
    
    credits: {
        style: {
            color: '#aeb6b7',
            fontSize: '10px'
        }
    }
};

// Apply the theme
Highcharts.setOptions(Highcharts.theme);"""

        theme_file = self.output_dir / "js" / "cloudscape-highcharts-theme.js"
        theme_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(theme_file, 'w', encoding='utf-8') as f:
            f.write(theme_js)
        
        print(f"✅ Created Highcharts theme: {theme_file}")

    def create_integrated_examples(self):
        """Create example pages showing Cloudscape + Highcharts integration"""
        print("📄 Creating integration examples...")
        
        examples_dir = self.output_dir / "examples" / "integrated"
        examples_dir.mkdir(parents=True, exist_ok=True)
        
        # Create main example page
        example_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cloudscape + Highcharts Integration</title>
    
    <!-- Cloudscape Styles -->
    <link rel="stylesheet" href="../css/cloudscape-highcharts-integration.css">
    
    <!-- Highcharts -->
    <script src="https://code.highcharts.com/highcharts.js"></script>
    <script src="https://code.highcharts.com/modules/exporting.js"></script>
    <script src="https://code.highcharts.com/modules/export-data.js"></script>
    <script src="https://code.highcharts.com/modules/accessibility.js"></script>
    
    <!-- Custom Theme -->
    <script src="../js/cloudscape-highcharts-theme.js"></script>
    
    <style>
        body {
            font-family: "Amazon Ember", "Helvetica Neue", Roboto, Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #fafbfc;
            color: #16191f;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        
        .header {
            background: #ffffff;
            padding: 24px;
            border-radius: 8px;
            margin-bottom: 24px;
            border: 1px solid #d5dbdb;
        }
        
        .grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 24px;
            margin-bottom: 24px;
        }
        
        @media (max-width: 768px) {
            .grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Cloudscape + Highcharts Design System</h1>
            <p>Integration of your original Cloudscape Design System with Highcharts charting library. 
            All charts use design tokens and styling that match your design system.</p>
        </div>
        
        <div class="grid">
            <div class="cloudscape-chart-container">
                <h2 class="cloudscape-chart-title">Revenue Trends</h2>
                <p class="cloudscape-chart-description">Monthly revenue showing growth trajectory</p>
                <div id="chart1"></div>
            </div>
            
            <div class="cloudscape-chart-container">
                <h2 class="cloudscape-chart-title">Service Distribution</h2>
                <p class="cloudscape-chart-description">Breakdown of services by usage</p>
                <div id="chart2"></div>
            </div>
        </div>
        
        <div class="cloudscape-chart-container">
            <h2 class="cloudscape-chart-title">Performance Metrics</h2>
            <p class="cloudscape-chart-description">System performance over time with multiple metrics</p>
            <div id="chart3"></div>
        </div>
    </div>

    <script>
        // Line chart with Cloudscape styling
        Highcharts.chart('chart1', {
            title: {
                text: 'Monthly Revenue'
            },
            xAxis: {
                categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            },
            yAxis: {
                title: {
                    text: 'Revenue ($M)'
                }
            },
            series: [{
                name: '2024',
                data: [29.9, 71.5, 106.4, 129.2, 144.0, 176.0, 135.6, 148.5, 216.4, 194.1, 95.6, 54.4]
            }, {
                name: '2023',
                data: [24.5, 65.2, 89.1, 102.3, 125.7, 142.8, 120.1, 135.2, 189.7, 172.4, 89.2, 48.1]
            }]
        });

        // Pie chart
        Highcharts.chart('chart2', {
            chart: {
                type: 'pie'
            },
            title: {
                text: 'Service Usage'
            },
            tooltip: {
                pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
            },
            plotOptions: {
                pie: {
                    allowPointSelect: true,
                    cursor: 'pointer',
                    dataLabels: {
                        enabled: true,
                        format: '<b>{point.name}</b>: {point.percentage:.1f} %'
                    }
                }
            },
            series: [{
                name: 'Services',
                colorByPoint: true,
                data: [{
                    name: 'EC2',
                    y: 45.8
                }, {
                    name: 'S3',
                    y: 26.3
                }, {
                    name: 'Lambda',
                    y: 12.2
                }, {
                    name: 'RDS',
                    y: 8.7
                }, {
                    name: 'Other',
                    y: 7.0
                }]
            }]
        });

        // Multi-series area chart
        Highcharts.chart('chart3', {
            chart: {
                type: 'area'
            },
            title: {
                text: 'System Performance'
            },
            xAxis: {
                categories: ['00:00', '04:00', '08:00', '12:00', '16:00', '20:00']
            },
            yAxis: {
                title: {
                    text: 'Percentage'
                }
            },
            tooltip: {
                shared: true,
                valueSuffix: '%'
            },
            plotOptions: {
                area: {
                    stacking: 'normal',
                    lineColor: '#ffffff',
                    lineWidth: 1
                }
            },
            series: [{
                name: 'CPU Usage',
                data: [45, 52, 68, 75, 82, 58]
            }, {
                name: 'Memory Usage',
                data: [32, 38, 45, 52, 61, 44]
            }, {
                name: 'Network I/O',
                data: [18, 22, 28, 35, 42, 28]
            }]
        });
    </script>
</body>
</html>"""

        example_file = examples_dir / "cloudscape-charts-demo.html"
        with open(example_file, 'w', encoding='utf-8') as f:
            f.write(example_html)
        
        print(f"✅ Created integration example: {example_file}")

def main():
    print("🔶 Highcharts + Cloudscape Integration")
    print("Combining the extracted Cloudscape materials with Highcharts")
    print()
    
    integrator = HighchartsCloudscapeIntegrator()
    integrator.integrate_all()
    
    print()
    print("🎯 Integration Results:")
    print("• Cloudscape CSS/SCSS files copied and organized")
    print("• Highcharts assets integrated")
    print("• Design token mapping created")
    print("• Custom Cloudscape theme for Highcharts")
    print("• Working example pages with charts")
    print()
    print("📁 Check refined_materials/integrated_design_system/")
    print("🌐 Open examples/integrated/cloudscape-charts-demo.html to see it in action!")

if __name__ == "__main__":
    main()