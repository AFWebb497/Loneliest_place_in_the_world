This project is centred around the goal of identifying the most isolated point on
Earth’s surface, where one could be furthest away from all other human
population centers. We began with a vague question that required precise
formalization, ultimately defining our goal as finding the point(s) on land
that maximize the distance from human population centers, using publicly
accessible data.
The journey to answer this involved several key phases, starting with the search for
a suitable dataset and the acquisition of the necessary data manipulation
skills. Once armed with the data, we devised and refined methodologies to
calculate the distance of any given point from human population settlements
and determine how to maximize this distance. Various approaches were
tested, considering both success and computational efficiency.

As we progressed, the challenge of implementing our methodology on a
global scale became evident. The sheer size of the dataset compelled us to
divide it, a decision not without its own challenges. However, we persevered
and successfully applied our approach to the entire dataset.
With the final dataset in hand, we introduced filters to evaluate each
point’s suitability as the most isolated location. Through rigorous analysis,
we identified one final candidate, which we believe represents the loneliest
place on Earth with a reasonable degree of confidence. This conclusion is
substantiated by the criteria we established and the data-driven process we
followed.

In closing, our project has not only answered a unique and intriguing
question but has also demonstrated the power of data-driven analysis in
solving complex geographical inquiries. We hope that our work serves as a
foundation for future investigations into understanding the remotest places
on our planet.

The code candidateGeneration requires the GHSL Global POP dataset, foudn at the following url:

https://ghsl.jrc.ec.europa.eu/download.php?ds=pop

The data generated is provided in the form of a series of text files, which are processed by the visualisation.ipynb jupyter notebook file.
