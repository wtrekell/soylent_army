/* *
 *
 *  License: www.highcharts.com/license
 *
 *  !!!!!!! SOURCE GETS TRANSPILED BY TYPESCRIPT. EDIT TS FILE ONLY. !!!!!!!
 *
 * */

/* *
 *
 *  Imports
 *
 * */

import type {
    SMAOptions,
    SMAParamsOptions
} from '../SMA/SMAOptions';

/* *
 *
 *  Declarations
 *
 * */

export interface TrendLineParamsOptions extends SMAParamsOptions {
    // For inheritance
    index: number;
}

export interface TrendLineOptions extends SMAOptions {
    params?: TrendLineParamsOptions;
}

/* *
 *
 *  Default Export
 *
 * */

export default TrendLineOptions;
