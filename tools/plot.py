#!/usr/bin/env python
# encoding: utf8


# System imports
import argparse
from os import makedirs
from os.path import join, exists, isdir
from itertools import product, chain
from math import sqrt
from copy import copy

# Six imports
from six import itervalues
from six.moves import range

# owls-cache imports
from owls_cache.persistent import caching_into

# owls-parallel imports
from owls_parallel import ParallelizedEnvironment

# owls-hep imports
from owls_hep.module import load as load_module
from owls_hep.uncertainty import uncertainty_band, combined_uncertainty_band, \
    ratio_uncertainty_band, to_overall, sum_quadrature
from owls_hep.plotting import Plot, histogram_stack, combined_histogram, \
    ratio_histogram
from owls_hep.utility import integral, get_bins_errors

Plot.PLOT_HEADER_HEIGHT = 500
Plot.PLOT_LEGEND_LEFT = 0.70

# Parse command line arguments
parser = argparse.ArgumentParser(
    description = 'Generate plots and a combined plotbook'
)
parser.add_argument('-o',
                    '--output',
                    default = 'plots',
                    help = 'the plot output directory',
                    metavar = '<output>')
parser.add_argument('-M',
                    '--model-file',
                    required = True,
                    help = 'the path to the model definition module',
                    metavar = '<model-file>')
parser.add_argument('-m',
                    '--model',
                    required = True,
                    help = 'the model to plot',
                    metavar = '<model>')
parser.add_argument('-R',
                    '--regions-file',
                    required = True,
                    help = 'the path to the region definition module',
                    metavar = '<regions-file>')
parser.add_argument('-r',
                    '--regions',
                    nargs = '+',
                    help = 'the regions to plot',
                    metavar = '<region>')
parser.add_argument('-D',
                    '--distributions-file',
                    required = True,
                    help = 'the path to the histograms definition module',
                    metavar = '<distributions-file>')
parser.add_argument('-d',
                    '--distributions',
                    nargs = '+',
                    help = 'the histograms to plot',
                    metavar = '<distribution>')
parser.add_argument('-E',
                    '--environment-file',
                    required = True,
                    help = 'the path to the environment definition module',
                    metavar = '<environment-file>')
parser.add_argument('-t',
                    '--text-counts',
                    action = 'store_true',
                    help = 'enable text output of counts')
parser.add_argument('-n',
                    '--no-counts',
                    action = 'store_true',
                    help = 'disable event counts in legends')
parser.add_argument('-p',
                    '--publish',
                    action = 'store_true',
                    help = 'make plots for publishing')
parser.add_argument('-e',
                    '--error-label',
                    default = 'Stat. Unc.',
                    help = 'the label to use for error bands',
                    metavar = '<error-label>')
parser.add_argument('--ratio-title',
                    default = 'Data / Background',
                    help = 'Y-axis title to use for the ratio histogram',
                    metavar = '<ratio-title>')
parser.add_argument('-l',
                    '--label',
                    nargs = '*',
                    help = 'items to add to the custom label',
                    metavar = '<items>')
parser.add_argument('-a',
                    '--atlas-label',
                    default = None,
                    help = 'the label to use for the ATLAS stamp',
                    metavar = '<atlas-label>')
parser.add_argument('-x',
                    '--extensions',
                    nargs = '+',
                    default = ['pdf'],
                    help = 'save these extensions (default: pdf)')
parser.add_argument('definitions',
                    nargs = '*',
                    help = 'definitions to use within modules in the form x=y',
                    metavar = '<definition>')
arguments = parser.parse_args()

# Style for tau triger public plots
# TODO: Plotting style should be more configurable
if arguments.publish:
    Plot.PLOT_MARGINS_WITH_RATIO = (0.125, 0.025, 0.025, 0.025)
    Plot.PLOT_RATIO_MARGINS = (0.125, 0.025, 0.325, 0.035)
    Plot.PLOT_HEADER_HEIGHT = 450 # px
    Plot.PLOT_LEGEND_TOP_WITH_RATIO = 0.95
    Plot.PLOT_LEGEND_LEFT = 0.62
    Plot.PLOT_LEGEND_TEXT_SIZE_WITH_RATIO = 0.055
    Plot.PLOT_LEGEND_ROW_SIZE_WITH_RATIO = 0.08
    Plot.PLOT_ATLAS_STAMP_TOP_WITH_RATIO = 0.88
    Plot.PLOT_ATLAS_STAMP_LEFT = 0.18
    Plot.PLOT_ATLAS_STAMP_TEXT_SIZE_WITH_RATIO = 0.065
    Plot.PLOT_RATIO_Y_AXIS_MINIMUM = 0.6
    Plot.PLOT_RATIO_Y_AXIS_MAXIMUM = 1.4
    Plot.PLOT_RATIO_Y_AXIS_NDIVISIONS = 204

    Plot.PLOT_ERROR_BAND_FILL_STYLE = 3013
    Plot.PLOT_ERROR_BAND_FILL_COLOR = 1
    Plot.PLOT_RATIO_ERROR_BAND_FILL_STYLE = 3001
    Plot.PLOT_RATIO_ERROR_BAND_FILL_COLOR = 632

# Parse definitions
definitions = dict((d.split('=') for d in arguments.definitions))


# Load files
model_file = load_module(arguments.model_file, definitions)
regions_file = load_module(arguments.regions_file, definitions)
distributions_file = load_module(arguments.distributions_file, definitions)
environment_file = load_module(arguments.environment_file, definitions)


# Extract model
model = getattr(model_file, arguments.model)
luminosity = model['luminosity']
sqrt_s = model['sqrt_s']
if model.has_key('data'):
    data = model['data']
else:
    data = None

if model.has_key('signals'):
    signals = model['signals']
else:
    signals = {}
backgrounds = model['backgrounds']

# Extract regions
regions = dict((
    (r, getattr(regions_file, r))
    for r
    in arguments.regions
))


# Extract histogram distributions
distributions = dict((
    (d, getattr(distributions_file, d))
    for d
    in arguments.distributions
))

# Get computation environment
cache = getattr(environment_file, 'persistent_cache', None)
backend = getattr(environment_file, 'parallelization_backend', None)

# Create the parallelization environment
parallel = ParallelizedEnvironment(backend)

# Create output directories
for region_name in regions:
    # Compute the region's output path
    region_path = join(arguments.output, region_name)

    # Try to create it
    if not exists(region_path):
        makedirs(region_path)


# Run in a cached environment
with caching_into(cache):
    # Run in a parallelized environment
    while parallel.run():
        if parallel.computed():
            print('Creating plots...')

        # Loop over regions and distributions
        for region_name, distribution_name in product(regions, distributions):
            # Grab the region/distribution objects
            region = regions[region_name]
            distribution = distributions[distribution_name]

            # Create the data histogram
            data_histogram = None
            if data is not None:
                data_process = data['process']
                data_estimation = data['estimation']
                data_histogram = data_estimation(distribution)(
                    data_process,
                    region
                )
                # data_histogram.SetTitle('Data')

                # If this region is blinded, then zero-out the data histogram
                if region.metadata().get('blinded', False):
                    data_histogram.Reset('M')

            # Initialize signal and background counts
            signal_count = 0
            background_count = 0

            # Create the signal histogram
            signal_histograms = []
            signal_uncertainty_bands = []
            for signal in itervalues(signals):
                # Extract parameters
                process = signal['process']
                estimation = signal['estimation']

                # Compute the histogram
                histogram = estimation(distribution)(process, region)
                signal_histograms.append(histogram)

                # Add to the signal count
                signal_count += integral(histogram, False)

                # NOTE: We use only statistical uncertainties only for the
                # signal. This can be expanded to include systematic
                # uncertainties when necessary.
                # Compute statistical uncertainties
                signal_uncertainty_bands.append(
                    uncertainty_band(
                        process,
                        region,
                        distribution,
                        None,
                        estimation
                    )
                )

            # Loop over background samples and compute their histograms
            background_histograms = []
            background_uncertainty_sizes = []
            background_uncertainty_bands = []
            for background in itervalues(backgrounds):
                # Extract parameters
                process = background['process']
                estimation = background['estimation']
                uncertainties = background.get('uncertainties', [])

                # Compute the nominal histogram
                histogram = estimation(distribution)(process, region)
                background_histograms.append(histogram)

                # Add to the signal or background count
                if background.get('treat_as_signal', False):
                    signal_count += integral(histogram, False)
                else:
                    background_count += integral(histogram, False)

                # Set up error bands
                sample_uncertainty_bands = []
                sample_uncertainty_sizes = {}

                # Compute statistical uncertainties
                sample_uncertainty_bands.append(
                    uncertainty_band(
                        process,
                        region,
                        distribution,
                        None,
                        estimation
                    )
                )

                # Compute systematic uncertainties
                for uncertainty in uncertainties:
                    overall_up, overall_down, shape_up, shape_down = \
                            estimation(uncertainty(distribution))(process, region)
                    up_variations = []
                    down_variations = []
                    if overall_up is not None:
                        up_variations.append(overall_up-1.0)
                    if shape_up is not None:
                        up_variations.append(to_overall(shape_up, histogram)-1.0)
                    if overall_down is not None:
                        down_variations.append(1.0-overall_down)
                    if shape_down is not None:
                        down_variations.append(1.0-to_overall(shape_down, histogram))
                    sample_uncertainty_sizes[uncertainty.name] = (
                        sum_quadrature(up_variations),
                        sum_quadrature(down_variations)
                    )
                    sample_uncertainty_bands.append(
                        uncertainty_band(
                            process,
                            region,
                            distribution,
                            uncertainty,
                            estimation
                        )
                    )

                # Combine the uncertainties for this process
                if len(sample_uncertainty_bands) > 0:
                    background_uncertainty_bands.append(
                        combined_uncertainty_band(sample_uncertainty_bands)
                    )
                background_uncertainty_sizes.append(sample_uncertainty_sizes)

            # If we're in capture mode, the histograms are bogus, so ignore
            # them
            if parallel.capturing():
                continue

            # Create combined background and signal histograms
            background_histogram = combined_histogram(background_histograms)
            background_histogram.SetTitle('Total background')
            if len(signal_histograms):
                signal_histogram = combined_histogram(signal_histograms)
                signal_histogram.SetTitle('Total signal')
            else:
                signal_histogram = None

            # Add text output if requested
            # TODO: REFACTOR THIS
            if arguments.text_counts:
                # Compute the text output path
                text_output_path = join(arguments.output,
                                        region_name,
                                        '{0}.txt'.format(distribution_name))

                # Save text
                with open(text_output_path, 'w') as f:
                    # Calculate s/sqrt(b)
                    if background_count != 0.0:
                        try:
                            f.write('s/sqrt(b): {0:.2f}\n'. \
                                    format(signal_count /
                                           sqrt(background_count)))
                        except ValueError:
                            pass
                        f.write('s/sqrt(s+b): {0:.2f}\n\n'. \
                                format(signal_count /
                                       sqrt(signal_count + background_count)))
                    else:
                        f.write('b = 0.0, no s/sqrt(b)\n\n')

                    # Print out uncertainty sizes per histogram
                    for h,uncertainties in zip(background_histograms,
                                               background_uncertainty_sizes):
                        if h is None:
                            continue

                        f.write('--- {} ---\n'.format(h.GetTitle()))
                        for u,v in sorted(uncertainties.items()):
                            f.write('{:20s}: ({:.3f}, {:.3f})\n'.format(u, *v))
                        f.write('\n')

                    # Print out histogram content
                    for h in chain((data_histogram,
                                    signal_histogram,
                                    background_histogram),
                                   signal_histograms,
                                   background_histograms):
                        if h is None:
                            continue

                        f.write('--- {} ---\n'.format(h.GetTitle()))
                        f.write('Entries:  {:.1f}\n'.format(h.GetEntries()))
                        f.write('Integral: {:.1f}\n'.format(integral(h, False)))
                        f.write('Overflow: {:.1f}\n'.format(integral(h, True)))
                        for i, (b,v,e) in zip(range(h.GetNbinsX()+2),
                                                    get_bins_errors(h, True)):
                            f.write('{:4d} ({:5.1f}, {:6.1f}±{:.1f})\n'. \
                                    format(i, b, v, e))
                        f.write('\n')

            # Set all histogram titles to include their counts
            if not arguments.no_counts:
                for h in chain((data_histogram,),
                               signal_histograms,
                               background_histograms):
                    if h is None:
                        continue

                    h.SetTitle('{0} ({1:.1f})'. \
                               format(h.GetTitle(), integral(h, False)))

            # Create a plot
            plot = Plot('',
                        distribution.x_label(),
                        distribution.y_label(),
                        ratio = (data is not None))

            # Plot data with background subtraction vs signal
            if signal_histogram is not None \
               and model.get('subtract_background', False):
                # Create a signal stack
                signal_stack = histogram_stack(*signal_histograms)

                # Compute combined uncertainties on the signal
                uncertainty = combined_uncertainty_band(
                    signal_uncertainty_bands,
                    signal_histogram,
                    arguments.error_label
                )
                ratio_uncertainty = ratio_uncertainty_band(
                    signal_histogram,
                    uncertainty
                )

                # Subtract background from data
                data_histogram = data_histogram - background_histogram

                # Draw the histograms
                plot.draw(((signal_stack, uncertainty), None, 'hist'),
                          (data_histogram, None, 'ep'))

                # Draw the ratio plot
                if data_histogram is not None:
                    ratio = ratio_histogram(data_histogram,
                                            signal_stack,
                                            arguments.ratio_title)
                    plot.draw_ratio_histogram(ratio,
                                              error_band = ratio_uncertainty)

                legend_entries = (data_histogram,
                                  signal_stack,
                                  uncertainty)

            # Plot data vs background model with optional signal overlay
            else:

                # Create a background stack
                background_stack = histogram_stack(*background_histograms)

                # Compute combined uncertainties
                uncertainty = combined_uncertainty_band(
                    background_uncertainty_bands,
                    background_histogram,
                    arguments.error_label
                )
                ratio_uncertainty = ratio_uncertainty_band(
                    background_histogram,
                    uncertainty
                )

                # Draw the histograms
                plot.draw(((background_stack, uncertainty), None, 'hist'),
                          (signal_histogram, None, 'hist'),
                          (data_histogram, None, 'ep'))

                # Draw the ratio plot
                if data_histogram is not None:
                    ratio = ratio_histogram(data_histogram,
                                            background_stack,
                                            arguments.ratio_title)
                    plot.draw_ratio_histogram(ratio,
                                              error_band = ratio_uncertainty)

                legend_entries = (data_histogram,
                                  signal_histogram,
                                  background_stack,
                                  uncertainty)

            # Draw a legend
            plot.draw_legend(legend_entries = legend_entries)

            # Draw an ATLAS stamp
            label = copy(region.label())
            if arguments.label:
                label += arguments.label
            plot.draw_atlas_label(luminosity,
                                  sqrt_s,
                                  custom_label = label,
                                  atlas_label = arguments.atlas_label)

            # Compute the plot output path
            plot_output_path = join(arguments.output,
                                    region_name,
                                    distribution_name)

            # Save plot
            plot.save(plot_output_path, arguments.extensions)
