# The JSON Colormap format, version v0.1-DRAFT

Authors: Nathaniel J. Smith <njs@pobox.com>

Version: v0.1-DRAFT

Stability: It's a draft. Anything may change. ANYTHING.


## Abstract

There's currently no standard interchange format for colormaps; every
time you want to design a new colormap or use it to some new tool,
then you have to write Yet Another Boring Conversion Script. For
example, currently [ColorBrewer](http://colorbrewer2.org/) provides
colormaps in 6 different formats, mostly ad hoc, and Peter Kovesi
provides his colormaps in in
[14 different vendor-specific formats](http://peterkovesi.com/projects/colourmaps/index.html)
-- and yet this still doesn't include any formats that are supported
by popular software like D3 or Matplotlib.

We propose the JSON Colormap (JSON-CM) format as a method for storing
and interchanging colormaps between different systems.


## Language

The key words “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”,
“SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “MAY”, and “OPTIONAL” in this
document are to be interpreted as described in
[RFC 2119](https://www.ietf.org/rfc/rfc2119.txt).


## Goals and scope

JSON-CM files are designed to:
- handle both discrete and continuous colormaps,
- be interoperable across a wide range of implementations,
- be suitable both for interchange and as a native storage format,
- include enough metadata to help users browse and select an
  appropriate colormap for their application, and
- be reasonably compact, to allow direct use in web-based
  visualizations that are sensitive to download size.


## Overview

JSON-CM files use the [JSON](http://www.json.org/) format as specified
by
[ECMA-404](http://www.ecma-international.org/publications/files/ECMA-ST/ECMA-404.pdf). Here's
an example `viridis.jscm` that uses all features (with some portions
replaced by ... ellipses):

```json
{
    "content-type": "application/vnd.matplotlib.colormap-v1+json",

    "name": "viridis",
    "license": "http://creativecommons.org/publicdomain/zero/1.0/",
    "usage-hints": ["sequential", "red-green-colorblind-safe", "greyscale-safe"],

    "description":
        "A perceptually uniform colormap designed to make a good default",
    "credit": "Eric Firing, Nathaniel J. Smith, Stéfan van der Walt",
    "citations": [ ... ],

    "domain": "continuous",
    "colorspace": "sRGB",
    "colors": "aabbccaabbccaabbccaabbcc...",

    "extensions": {
        "http://matplotlib.org/viscm": {
            "spline-control-points": ...,
            ...
        }
    }
}
```

When stored on disk, JSON-CM files SHOULD use UTF-8 and the `.jscm`
extension.

The MIME type for JSON-CM files is: `application/vnd.matplotlib.colormap-v1+json`

(TODO: there isn't intended to be anything matplotlib specific about
this specification, but "vnd" MIME types are required to start with
the name of a well-known vendor/organization that implements the
spec. So matplotlib seems like an obvious choice -- it's certainly not
worth founding and naming a new cross-project organization just to
host this spec! -- but if anyone has a better idea let me know.)


## Contents

Each JSON-CM file consists of a single top-level JSON object, which
contains a number of key/value entries. Some keys are mandatory: they
MUST be included in compliant JSON-CM files, and JSON-CM readers SHOULD
reject any file missing them. Other keys are optional; compliant JSON-CM
files MAY include them, but JSON-CM readers MUST NOT reject a file for
missing them.


### Metadata

These keys give metadata about the colormap:

* **`"content-type"`** (mandatory): This key MUST have the value
  `"application/vnd.matplotlib.colormap-v1+json"`, and JSON-CM readers MUST
  check for and reject any file where this value is missing or
  different.

* **`"name"`** (mandatory): A short string giving the name of this
  colormap. For maximum interoperability, this SHOULD be a string of
  lowercase alphanumeric characters that starts with a alphabetic
  character and contains no spaces.

* **`"license"`** (mandatory): A string containing a URL pointing to the
  license governing use of this colormap. (We're not convinced that
  colormaps even are governed by copyright or other intellectual
  property law, but since this is unclear it's best to be explicit.)

* **`"usage-hints"`** (mandatory): A list of strings containing tags
  that hint how this colormap is intended to be used. These tags are
  drawn from the following list:

  * Colormap types:
    * `"sequential"`: indicates that this colormap is suitable for
      representing sequentially ordered data.
    * `"diverging"`: indicates that this colormap is suitable for
      representing data in which there is a privileged point
      corresponding to the center of the colormap, and in which the
      viewer's attention should be drawn to deviations above and below
      this center point.
    * `"cyclic"`: indicates that this colormap is suitable for
      representing data in which the lowest and highest values are
      equivalent (for example, angles).
    * `"qualitative"`: indicates that this colormap is suitable for
      representing data consisting of a collection of discrete
      categories. (This tag SHOULD only be used with colormaps that have
      `"domain": "discrete"` -- see below.)
  * `"isoluminant"`: indicates that this colormap avoids using the
    lightness channel to convey information, and thus may be suitable
    for use in contexts where the lightness channel is used
    independently for representing other data, such as relief shading.
  * `"red-green-colorblind-safe"`: indicates that this colormap's
    designers believe that visualizations using it will be interpretable
    by individuals with red-green colorblindness (i.e., deuteranomaly,
    deuteranopia, protanomaly, or protanopia).
  * `"greyscale-safe"`: indicates that this colormap's designers believe
    that visualizations using it will remain interpretable after being
    converted to greyscale.

  We anticipate that more tags may be added in the future.

  The `"usage-hints"` list MAY be empty, but SHOULD always contain at
  least one of the colormap type tags. (If you discover a new type of
  colormap that is not included above, please let us know so that we can
  add a tag for it to the list.)

* **`"description"`** (optional): A string containing a short description of
  this colormap and noting any special features or suggested
  usages. This should be written to aid a user who is scrolling through
  a variety of different colormaps and attempting to pick one.

* **`"credit"`** (optional): A free-form string giving credit to the
  colormap's designer(s).

* **`"citations"`** (optional): Gives a recommended citation or citations in
  case a user wants to credit this colormap. If present, it should be a
  list of JSON objects in
  [CSL-JSON format](https://github.com/citation-style-language/schema/blob/master/csl-data.json)
  (also known as "citeproc JSON format"). This is particularly intended
  to be useful in combination with tools like
  [duecredit](https://github.com/duecredit/duecredit) that provide
  automated mechanisms for tracking a project's tool-related citations.


### Data

These keys define the colormap itself:

* **`"colorspace"`** (mandatory): The colorspace to use for interpreting
  the color coordinates. Currently the only legal value is `"sRGB"`,
  meaning the
  [standard RGB space used by computer monitors](https://en.wikipedia.org/wiki/SRGB)
  as defined by IEC 61966-2-1:1999. Even though this is currently the
  only legal value, compliant readers MUST check for and reject any
  JSON-CM file where the `"colorspace"` is not `"sRGB"`, in order to
  allow for future extensions.

* **`"colors"`** (mandatory): The list of colors making up this
  colormap, represented as a string of concatenated hexadecimal
  digits. The digits `a`-`f` MUST be given in lowercase form, and the
  string length MUST be a multiple of six. Each group of six digits
  defines one sRGB color; for example, the string `"aabbcc112233778899"`
  defines a colormap containing the three colors `#aabbcc`, `#112233`,
  and `#778899` in the
  [standard HTML notation](https://html.spec.whatwg.org/#colours), or
  equivalently `rgb(170, 187, 204)`, `rgb(17, 34, 51)`, `rgb(119, 136,
  153)` in
  [CSS notation](https://drafts.csswg.org/css-color/#rgb-functions).

  *Rational for this encoding scheme:* JSON is rather verbose. This is
  good when it promotes human readability, but the color list is a large
  blob of essentially opaque data which makes up a large proportion of
  the file size. And given that we expect an important use case for
  these files to be web-based visualization tools like D3, we want to
  avoid unnecessarily bloating downloads. This table compares a number
  of possible encodings that were considered, along with the number of
  bytes needed to represent each color when written in their shortest
  legal form (so e.g. omitting spaces). "ABCDABCD..." is base64 encoding
  of each color into 4 bytes:

  | Encoding                   | Bytes per color | Relative overhead |
  | -------------------------- | ---------------:| -----------------:|
  | "ABCDABCDABCD..."          |               4 |              -33% |
  | "aabbccaabbcc..."          |               6 |                0% |
  | ["aabbcc","aabbcc", ...]   |               9 |              +50% |
  | ["#aabbcc","#aabbcc", ...] |              10 |              +67% |
  | [[.123,.123,.123],...]     |              17 |              +83% |

  We judge that base64 coding sufficiently unfamiliar and annoying to
  work with that it might pose an obstacle to wide adoption, while only
  saving 2 bytes per color. Compared to the adopted "aabbcc..."
  solution, the other options all add substantial overhead for almost no
  benefit. Additionally, there is prior art: this encoding is already
  used
  [internally by D3](https://github.com/d3/d3-scale/blob/081c4e51f7a7f284da85352350915a037d4e5301/src/viridis.js). And
  finally, if even smaller files are needed, then one can of course
  compress the JSON-CM file using a general-purpose compression tool. In
  fact, it turns out that in at least some cases this is another
  advantage of the JSON-CM encoding. For viridis with 256 listed colors
  we have, as expected:

  | Encoding              | Size (bytes) |
  | --------------------- | ------------:|
  | Raw binary            |          768 |
  | Base64                |         1024 |
  | JSON-CM hex           |         1536 |

  But if we apply DEFLATE compression (as used in gzip), we find that
  remarkably the JSON-CM hex encoding gives the *smallest*
  representation:

  | Encoding              | Size (bytes) |
  | --------------------- | ------------:|
  | Raw binary + DEFLATE  |          773 |
  | Base64 + DEFLATE      |          708 |
  | JSON-CM hex + DEFLATE |          674 |

  Presumably this is some side-effect of how hex encoding separates the
  low-order and high-order bits in each value, similar to how
  [shuffling in HDF5 improves compression](http://www.hdfgroup.org/HDF5/doc_resource/H5Shuffle_Perf.pdf).

* **`"domain"`** (mandatory): Value MUST be either the string
  `"discrete"`, or the string `"continuous"`, and specifies how to
  interpret the list of `"colors"`.

  In general, a colormap is a mapping from some kind of data to colors
  -- but there are different kinds of data. A `"discrete"` colormap maps
  a discrete set of data values into a discrete set of colors -- for
  example, if our example above defines a `"discrete"` colorspace, then
  category 1 maps to `#aabbcc`, category 2 maps to `#112233` and
  category 3 maps to `#778899`. It makes no sense to ask what color
  should be used for category 1.5. (A `"discrete"` colormap with the
  `"sequential"` `"usage-hint"` defines a set of ordered categories, and
  can be applied to continuous data by discretizing the data and then
  mapping each category to one of the listed colors in order.)

  A `"continuous"` colormap maps a continuous domain of data -- for
  example all values 0 through 1 -- into a continuous range of colors,
  and the listed `"colors"` define particular points in colorspace that
  the colormap interpolates between. For example, if our example above
  defines a `"continuous"` colorspace, then the value 0 maps to
  `#aabbcc`, the value 0.5 maps to `#112233`, the value 1 maps to
  `#778899`, the value 0.25 maps to the color midway between `#aabbcc`
  and `#112233`, and so forth. Interpolation SHOULD be performed in sRGB
  space.

  *Rationale for this representation of continuous colormaps:*
  Visualization tools often provide richer representations for
  representing colormaps, for example allowing the user to specify that
  interpolation should be performed in other colorspaces like
  [HSV](https://en.wikipedia.org/wiki/HSL_and_HSV), or allowing to
  directly specify the mapping between data points and colors, rather
  than requiring the colors to be evenly spaced as we do here. We avoid
  such features, because (a) we believe that keeping things simple has
  significant benefits for interoperability and adoption, and (b) we
  believe that these features provide relatively little value to
  compensate for their complexity: in our experience, good colormaps
  require more complex representations than we would want to inclue here
  in any case (e.g. spline curves in some more sophisticated color
  space) and need to be reduced to a fine RGB grid for actual usage
  anyway. And once you have a fine RGB grid, then details like the
  interpolation method don't really matter in practice. (We recommend
  the use of sRGB for interpolation for consistency between
  implementations; it's only a recommendation because we don't think it
  matters much, and some implementations may elect to use e.g. nearest
  neighbor instead for speed, so long as this produces comparable
  results.)


### Extensions

One key is reserved to provide a space for ad hoc and vendor-specific
extensions:

* **`"extensions"`** (optional): If present, the value associated with
  this key MUST be a JSON object, and each key in this object MUST be
  a URL that uniquely and durably identifies the format of the
  extension data associated with that key. This URL SHOULD refer to
  web page providing more information about this extension.

  For example, one of the motivating use cases for JSON-CM was to
  provide a format for the [viscm](https://github.com/matplotlib/viscm)
  colormap design tool to save its colormaps; in the example document
  given at the top of this file, you can see how viscm might use an
  extension field to store its internal data like spline control points
  that are needed to allow this colormap to be loaded back into the
  editor:

  ```json
  {
      ...
      "extensions": {
          "https://matplotlib.org/viscm": {
              ... viscm's internal representation of the colormap ...
          }
      }
  }
  ```


### Other keys

JSON-CM readers MUST accept and ignore any top-level keys which are not
specified above; these are reserved for future additions to this
specification.

JSON-CM writers MUST NOT use any top-level keys which are not
specified above; if you find the above keys insufficient, then you
should either propose an addition to this specification or else use an
`"extension"` key.


## JSON-Schema

Available [here](./json-cm-schema.json).

(TODO: test it)


## History

v0.1-DRAFT (2016-04-20): Initial release.


## License

This document is placed in the public domain.