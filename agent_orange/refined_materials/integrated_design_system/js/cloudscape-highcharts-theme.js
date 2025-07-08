/*
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
Highcharts.setOptions(Highcharts.theme);