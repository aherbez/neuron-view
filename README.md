# neuron-view

![example output](https://github.com/aherbez/neuron-view/blob/main/docs/neuron_view.png)

This is a tool to create 3d models from SWC neuron description files.

It is based around the excellent [SDF library](https://github.com/fogleman/sdf) created by Michael Fogleman

## Installation

To use the tool, start by cloning the repo, and navigate to the directory.

Then, create a virtual environment with:

`python -m venv venv`

Next, activate the environment with:

`./venv/scripts/activate`

Install dependencies with:

`pip install -r requirements.txt`

That might take a bit, but after that's done, you should be good to go.

## Usage 

To use the tool, you'll need a SWC file. There are a few in the `swcs` folder, all pulled from [neuromorph.org](http://www.nueromorpho.org).

Use the tool with:

`python neuronview.py [SWC file] [stride]`

The "stride" value controls how many points will be used for each section. 

### Why "stride" is a thing

It would be great to just generate the model all at once, but trying to generate a single SDF from something like 3k individual shapes tends to fall over. So instead, the tool generates multiple 3d models by processing a subset of the entries at a time. Once all of those are generated, you can use a tool like Blender to combine the models into a single mesh.

The "stride" value determines how many entries are processed at a time. I've had good success using 325 as a value, but your results may vary. Larger numbers were unsuccessful on my machine, fwiw (decently powerful gaming laptop from 2022).

# Example run

This is how I generated the model in the above screenshot.

First, I ran the script with:

`python .\neuronview.py './swcs/AX3_scaled.swc' 320`

The script will create an "output" folder, and within that, a folder for the specific file ("AW3_scaled", in this case). 

It will then run through the file, creating 3d models (STLs) for each part. The files will be named with the start and end id of the entries they include, such as:

- cell_1_321.stl
- cell_321_641.stl
- ...
- cell_2881_3176.stl

This will likely take a while to process- go get a cup of coffee.

Once it's all done, you'll have some number of STL files in output folder. Next, it's time to combine them.

An easy way to do this is to open up Blender, and import all of the created files. Note that you might have to hunt around a bit to find where they are (it seems like the data is often not centered).

Select all the parts, and use Ctrl-J to join them. This will give you a single model. Note that you'll have overlapping / intersecting parts, but they're not likely to be that noticable. If that's a problem for your application, try either using Boolean unions or go into sculpt mode and use voxelization. Both of those might be iffy for large datasets though, so be warned.

Once you've combined the parts, you'll probably want to reduce the polycount. The file in the "example" folder of this repo is the result of having added a "decimate" modifier in Blender with a ratio of 0.1.

# Known issues

Currently, the tool doesn't make use of the "type" parameter in the entries, just the position and radius. That's probably something that needs to change, but I need to better understanad what it means first.

Having to piece together a full model from pieces is defnitely annoying, but I do very much like the inherent organic and continuous surface that the SDF based approach provides. There are a couple of possibilities for fixing this:

- forgo SDF and generate the mesh directly. This is definitely doable, but might not produce as nice junctures where sections meet.
- incorporate a final step to combine all the generated models in the script itself. This should be doable with open3d or similar, and is what I'm leaning towards.
