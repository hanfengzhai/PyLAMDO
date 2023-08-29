function result = cut15(a)
    % Make a copy of the input array so as not to modify it directly
    result = a;
    % Find the indices where the values in the second column are greater than 15
    idx = result(:, 2) > 15;
    % Replace those values with 15
    result(idx, 2) = 15;
end
